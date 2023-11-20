import frappe 
import random
from frappe import _
from frappe.model.document import Document
from datetime import datetime, timedelta
import frappe.exceptions

# @frappe.whitelist(allow_guest=True)
@frappe.whitelist()
def action_list():
    try:
        if frappe.local.request.method != "GET":
            return "Only GET API"
        args = frappe.local.request.args
        if args.get("pagination"):
            pagination = args.get("pagination")
        
        # get only permitted workflow action
        action_list = permitted_workflow_action()

        frappe.local.response.data = action_list
    except Exception as e:
        print(e)

# get only permitted workflow action
def permitted_workflow_action():
    try:
        action_list = frappe.db.get_all("Workflow Action", 
        fields=["name", "reference_doctype", "reference_name", "modified_by", "discard"],
        filters=[{"status":"Open"},{"discard": "No"}],
        limit_page_length = "*")
        user = frappe.session.user
        permitted_action = []
        
        i = -1
        for entry in action_list:
            i = i + 1
            
            doc_entry = frappe.get_doc(entry["reference_doctype"], entry["reference_name"])
            
            if not doc_entry.has_permission("write"):
                continue

            if doc_entry.docstatus == 1 or doc_entry.docstatus == 2:
                continue

            if entry["reference_doctype"] == "Leave Application" and not doc_entry.leave_approver == user:
                continue

            permitted_action.append(action_list[i])
            j = len(permitted_action) - 1
            permitted_action[j]["current_state"] = doc_entry.workflow_state
            
            user_detail_qry = f"""SELECT
                    US.full_name,
                    RO.role
                FROM
                    `tabUser` US
                JOIN 
                    `tabHas Role` RO ON US.name = RO.parent
                WHERE
                    US.name = "{user}"; """
            user_details = frappe.db.sql(user_detail_qry, as_dict=True)
            role = set()
            for dt in user_details:
                role.add(dt["role"])
            permitted_action[j]["roles"] = role

            mod_user = frappe.get_doc("User", entry["modified_by"]).full_name
            permitted_action[j]["full_name"] = mod_user

            permitted_action[j]["logged_user"] = user_details[0]["full_name"]

            workflow_trasition_qry = f"""SELECT
                    WT.next_state as next_state,
                    WT.action,
                    WT.allowed as role_allowed,
                    WT.state as current_state
                FROM
                    `tabWorkflow Transition` WT
                JOIN 
                    `tabWorkflow` WF ON WF.name = WT.parent
                WHERE
                    WF.is_active = 1
                    AND WF.document_type = "{entry["reference_doctype"]}"
                    AND WT.allowed in ({', '.join(f'"{element}"' for element in permitted_action[j]["roles"])})
                    AND WT.state = "{doc_entry.workflow_state}"; """
            workflow_transition = frappe.db.sql(workflow_trasition_qry, as_dict=True)
            permitted_action[j]["workflow_transition"] = workflow_transition
        return permitted_action
    except Exception as e:
        print(e)




from frappe.website.utils import is_signup_disabled
import frappe.permissions
from frappe.utils import (escape_html)
from frappe.utils import escape_html, random_string
import frappe
from frappe import _

SOCAIL_MEDIA_PLATEFORM = {
    "1":"Google",
    "2":"Apple"
}
# @frappe.whitelist(allow_guest=True)
@frappe.whitelist(allow_guest=True)
def sign_up():
    try:
        if frappe.local.request.method != "POST":
            return {
                'status_code': 405,
                'message': 'Only POST requests are allowed'
            }
        body = frappe.local.form_dict
        if is_signup_disabled():
            return {
                'status_code': 403,
                'message': 'Sign Up is disabled'
            }
      
        user_count = frappe.db.sql("""SELECT  COUNT(*) FROM `tabUser` WHERE email = '{email}' OR mobile_no = '{mobile_no}'""".format(
            email=body.get("email"),
            mobile_no=body.get("phone_no")
            ))[0][0]
        print(user_count)
        if user_count > 0:
            return {
                "status_code" : 409,
                "message" : f"User already exists with this email  or phone number"
                }
        else:
            if frappe.db.get_creation_count("User", 60) > 300:
                return {
                    'status_code': 429,
                    'message' : 'Temporarily Disabled',
                    'details' : 'Too many users signed up recently. Registration is disabled. Please try again later.'
                }

            user = frappe.new_doc("User")
            user.update({
                "email": body.get("email"),
                "first_name": body.get("first_name"),
                "last_name": body.get("last_name"),
                "full_name": frappe.utils.escape_html(body.get("full_name")),
                "gender": body.get("gender"),
                "birth_date": body.get("birth_date"),
                "enabled": 1,
                "new_password": body.get("new_password", random_string(10)),
                "user_type": "System User",
                "role_profile_name": "notibell role profile"
            })

            is_table_already_exists = 0
            if body.get("social_media_platform"):
                if body.get("social_media_guid"):
                    if user.get("social_logins"):
                        for media in user.get("social_logins"):
                            if media.provider == SOCAIL_MEDIA_PLATEFORM[body.get("social_media_platform")]:
                                media.userid = body.get("social_media_guid")
                                is_table_already_exists = 1
                    if not is_table_already_exists:
                        user.append("social_logins", {
                            "provider": SOCAIL_MEDIA_PLATEFORM[body.get("social_media_platform")],
                            "userid": body.get("social_media_guid")
                        })
                        user.is_social_login = 1
                        user.is_verified = 1
                        user.new_password = "Qwerty@1234"
                        user.flags.ignore_permissions = True
                        user.flags.ignore_password_policy = True
                        user.send_welcome_email = False
                        user.save()
                        create_employee(user, doc=None)
                    

                        return {"status_code": 200, "message": "User signup successful"}
                    else:
                        return {"status_code": 400, "message": "Please provide the social media GUID"}
                else:
                    return {"status_code": 400, "message": "Please provide the social media GUID"}
            else:
                user.flags.ignore_permissions = True
                user.flags.ignore_password_policy = True
                user.insert()
                create_employee(user, doc=None)
                default_role = frappe.db.get_single_value("Portal Settings", "default_role")

                if default_role:
                    user.add_roles(default_role)

                if user.flags.email_sent:
                    return {
                        'status_code': 200,
                        'message': 'User registered successfully'
                    }
                else:
                    return {"status_code": 2, "message": _("Please ask your administrator to verify your sign-up")}

    except Exception as e:
        return {
            'status_code': 500,
            'message': 'Requird Fields Are Missing'
        }


def create_employee(user, doc):
    try:
        employee = frappe.new_doc('Employee')
        employee.update({
            "full_name": user.full_name,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_of_birth": user.birth_date,
            "gender": user.gender,
            "date_of_joining": frappe.utils.now_datetime(),
            "user_id": user.email,
            "company_email": user.email
        })
        employee.flags.ignore_mandatory = True
        employee.insert(ignore_permissions=True)

        return {
                'status_code': 200,
                'message': 'Employee registered successfully'
                }
    except Exception as e:
        print(f"Error creating employee: {str(e)}")








