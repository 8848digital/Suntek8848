app_name = "suntek8848"
app_title = "Suntek8848"
app_publisher = "gopal@8848digital.com"
app_description = "Custom Changes"
app_email = "gopal@8848digital.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "suntek8848",
# 		"logo": "/assets/suntek8848/logo.png",
# 		"title": "Suntek8848",
# 		"route": "/suntek8848",
# 		"has_permission": "suntek8848.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/suntek8848/css/suntek8848.css"
# app_include_js = "/assets/suntek8848/js/suntek8848.js"

# include js, css files in header of web template
# web_include_css = "/assets/suntek8848/css/suntek8848.css"
# web_include_js = "/assets/suntek8848/js/suntek8848.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "suntek8848/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Sales Order" : "public/js/sales_order.js",
              "Employee Advance" : "public/js/employee_advance.js",
              "Expense Claim": "public/js/expense_claim.js"}
# doctype_list_js = {"Delivery Request" : "public/js/delivery_request_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "suntek8848/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "suntek8848.utils.jinja_methods",
# 	"filters": "suntek8848.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "suntek8848.install.before_install"
# after_install = "suntek8848.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "suntek8848.uninstall.before_uninstall"
# after_uninstall = "suntek8848.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "suntek8848.utils.before_app_install"
# after_app_install = "suntek8848.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "suntek8848.utils.before_app_uninstall"
# after_app_uninstall = "suntek8848.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "suntek8848.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"Delivery Request": "suntek8848.suntek8848.permissions.delivery_request.update_permissions",
}
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Delivery Request": {
        "on_submit": "suntek8848.suntek8848.doctype.delivery_request.delivery_request.update_sales_order",
		"on_update_after_submit": "suntek8848.suntek8848.doctype.delivery_request.delivery_request.update_approver_field",
		# "on_cancel": "method",
		# "on_trash": "method"
	},
    "Sales Order": {
        "validate": "suntek8848.suntek8848.doc_events.sales_order.update_outstanding_amount",
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"suntek8848.tasks.all"
# 	],
# 	"daily": [
# 		"suntek8848.tasks.daily"
# 	],
# 	"hourly": [
# 		"suntek8848.tasks.hourly"
# 	],
# 	"weekly": [
# 		"suntek8848.tasks.weekly"
# 	],
# 	"monthly": [
# 		"suntek8848.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "suntek8848.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"hrms.hr.doctype.expense_claim.expense_claim.get_advances": "suntek8848.suntek8848.overrides.expense_claim.get_advances"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "suntek8848.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["suntek8848.utils.before_request"]
# after_request = ["suntek8848.utils.after_request"]

# Job Events
# ----------
# before_job = ["suntek8848.utils.before_job"]
# after_job = ["suntek8848.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"suntek8848.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = [
        {"dt": "Custom Field", "filters": [
                [
                    "name", "in", [
                        "Delivery Request-custom_payment_schedules",
                        "Delivery Request-custom_section_break_",
                        "Delivery Request-workflow_state1",
                        "Delivery Request-custom_delivery_request_purpose",
                        "Delivery Request-custom_payment_from_sales_order",
                        "Delivery Request-custom_approver",
                        "Sales Order-custom_outstanding",
                        "Employee Advance-custom_column_break_crsgc",
                        "Employee Advance-custom_advance_type",
                        "Company-custom_default_employee_other_expense_account"
                    ]
               ]
        ]},
        {"dt": "Workflow", "filters": [
            [
                "name", "in", [
                    "Delivery Request"
                ]
            ]
        ]},
        {"dt": "Property Setter", "filters": [
            [
                "name", "in", [
                    "Delivery Request-custom_section_break_-depends_on",
                    "Sales Order-payment_schedule-allow_on_submit",
                    "Sales Order-custom_outstanding-in_list_view",
                    "Delivery Request-custom_approver-in_list_view",
                    "Employee Advance-advance_account-default",
                    "Employee Advance-advance_account-fetch_from"
                ]
            ]
        ]}
]