# Sundayz - Ice Cream Parlor App 🍦
A simple, user-friendly app that lets customers explore flavors, view menu items &amp; place orders.

## Project (Vision)
### 1. Menu Management:
- getHome.py                                            | /GET
- getAllFlavor.py                                       | /GET
- addFlavor.py                                          | /POST
- updateFlavor.py                                       | /PATCH
- deleteFlavor.py                                       | /DELETE
- searchFlavor.py                                       | /POST

### 2. User Management:
- register.py (CREATE A NEW USER)                       | /POST
- login.py (AUTHENTICATE AND RETURN A SESSION OR TOKEN) | /POST
- profile.py (FETCH USER DETAILS)                       | /GET
- updateProfile.py (UPDATE USER DETAILS)                | /PATCH
- deleteProfile.py (DELETE USER ACCOUNT)                | /DELETE

### 3. Order Management:
- createOrder.py                                        | /POST
-> INPUT: List of menu items with quantities
-> OUTPUT: Order confirmation with order_id, total_price

- getAllOrders.py                                       | /GET
-> Admin only end-point to fetch all
-> OUTPUT: list of orders with order_id, user_details, items, status and timestamp

- getUserOrders.py                                      | /GET
-> fetch all orders placed by logged-in user
-> OUTPUT: list order_id, items, total_price and status

- updateOrderStatus.py                                  | /PATCH
-> Admin only to update the status of an order (e.g. Preparing, Ready, Completed)
-> INPUT: order_id and new_status
-> OUTPUT: confirmation of status update

- deleteOrder.py                                        | /DELETE
-> allow admin and users both to cancel an order
-> INPUT: order_id
-> OUTPUT: confirmation of order deletion

- getOrderDetails.py                                    | /GET
-> fetch details of a specific order
-> INPUT: order_id
-> OUTPUT: order details (items, quantities, price and status)