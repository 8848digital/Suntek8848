## Suntek8848

## Delivery Request Doctype Changes

This update enhances the Delivery Request Doctype in Frappe/ERPNext by adding functionality to:

Fetch Sales Order Terms and display them in the child table.

Update Sales Order Terms via the Delivery Request.

Implement validation for Actual Amount.

Apply conditions based on a Select Field.

Apply permissions

Custom List View Fields

# Features Implemented

1. Fetch and Display Sales Order Terms in Child Table

When a Get Sales Order TErns button  is clicked, its terms are automatically fetched.

The fetched terms are displayed in a child table under the Delivery Request.

2. Update Sales Order Terms via Delivery Request

The terms of the linked Sales Order can be updated directly from the Delivery Request.

Changes in the Delivery Request terms are reflected in the associated Sales Order.

3. Validation for Actual Amount

Ensures that the Actual Amount does not exceed a predefined threshold.

If validation fails, an error message prevents submission.

4. Conditional Logic Based on Select Field

Business rules are applied based on the value selected in a specific field.

This ensures correct workflow execution.

5. Permission Update in Delivery Request Based on Org Cycle Report

Delivery Request permissions are now dynamically updated based on Org Cycle Report.

Access restrictions and approvals are aligned with organizational policies.

6. Add Custom List View in Delivery Request and Sales Order

## Customization in Employee Advance Doctype

1. Modifications made to the Advance Account field to improve data accuracy.

Ensures better account mapping and prevents incorrect entries.

2. Apply Filters in Expense Claim Based on Other Expenses

Filters are applied in Expense Claim to dynamically adjust options based on Other Expenses.

Enhances accuracy and prevents irrelevant selections.

## Procurement Cycle Lead Time Report
The Procurement Lead Time Report provides insights into the time taken for procurement processes, from purchase order to purchase and MR to PO receipt. This report helps in analyzing vendor performance, identifying delays, and improving procurement efficiency.

## Consolidation of items in PO print format

#### License

mit