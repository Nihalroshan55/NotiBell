from . import __version__ as app_version

app_name = "notibell"
app_title = "NotiBell"
app_publisher = "NestorBird"
app_description = "This app will add features through mobile App NotiBell with Push Notifications, Entry Approval-Rejection, applying aand "
app_email = "info@nestorbird.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/notibell/css/notibell.css"
# app_include_js = "/assets/notibell/js/notibell.js"

# include js, css files in header of web template
# web_include_css = "/assets/notibell/css/notibell.css"
# web_include_js = "/assets/notibell/js/notibell.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "notibell/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

doc_events={
    "Workflow Action":{
        "validate":"notibell.overrides.custom_workflow_action.validate"
    },
    "Employee": {
        "validate":"notibell.customizations.employee.validate"
    },
    "Employee Checkin": {
        "validate":"notibell.customizations.employee_checkin.validate"
    }
}


# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "notibell.utils.jinja_methods",
#	"filters": "notibell.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "notibell.install.before_install"
# after_install = "notibell.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "notibell.uninstall.before_uninstall"
# after_uninstall = "notibell.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "notibell.utils.before_app_install"
# after_app_install = "notibell.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "notibell.utils.before_app_uninstall"
# after_app_uninstall = "notibell.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "notibell.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"notibell.tasks.all"
#	],
#	"daily": [
#		"notibell.tasks.daily"
#	],
#	"hourly": [
#		"notibell.tasks.hourly"
#	],
#	"weekly": [
#		"notibell.tasks.weekly"
#	],
#	"monthly": [
#		"notibell.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "notibell.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "notibell.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "notibell.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["notibell.utils.before_request"]
# after_request = ["notibell.utils.after_request"]

# Job Events
# ----------
# before_job = ["notibell.utils.before_job"]
# after_job = ["notibell.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]


fixtures = [
    {
        "dt": "Custom Field",
        "filters": {
            "name": [
                "in",
                [
                   "Workflow Action-discard",
                    "Employee Checkin-custom_face_detection",
                    "Employee Checkin-custom_face_status",
                    "Employee Checkin-custom_latitude",
                    "Employee Checkin-custom_longitude",
                    "Employee Checkin-custom_location_status",
                    "Employee Checkin-custom_section_break_uj8ct",
                    "Employee Checkin-custom_column_break_hc88f",
                    "Employee-custom_face_registration",
                    "Employee-custom_face_registration_data"
                ]
            ]
        }
    },
    {
        "dt": "Custom DocPerm",
        "filters": {
            "name": [
                "in",
                [
                    "6a3d8081dd"
                ]
            ]
        }
    },
    {
        "dt": "Role Profile",
        "filters": {
            "name":[
                "in",
                [
                    "notibell role profile"
                ]
            ]
    }
    }
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"notibell.auth.validate"
# ]
