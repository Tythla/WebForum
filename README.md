# WebForum
## Name: Yonghao Zhang, Yangbo Liu
## Stevens login: yzhang8, yliu8
##  URL: 
https://github.com/Tythla/WebForum
##  Time spent: 22h
##  Code test:
To ensure the robustness and functionality of the web application, a comprehensive testing strategy was implemented. The tests focused on both the backend logic (using the `UserManager` class) and the Flask API endpoints. The testing was conducted using Python's `unittest` framework.
###  Backend Logic Testing
1.  **User Creation**: Verified the successful creation of users and the uniqueness of their usernames.
2.  **Moderator Creation**: Tested the creation of moderators, ensuring they are assigned unique moderator keys.
3.  **User Validation**: Checked the validation functionality with correct and incorrect keys.
4.  **User Retrieval**: Assessed the ability to retrieve user details using their user ID.
###  API Endpoint Testing
1.  **User Creation Endpoint**: Tested the user creation endpoint for successful user registration.
2.  **Moderator Creation Endpoint**: Verified the moderator creation endpoint, focusing on access control using the `Admin-Key`.
3.  **Post Creation and Deletion**: Ensured that posts could be created and deleted successfully, validating the correct use of user and moderator keys.
##  Bugs and issues not resolve: 
None
##  A difficult issue resolved:
One of issue we met was encountered with user authentication. 
Solution: 
1.  Implemented a utility function to correctly format and process the user keys extracted from API requests, ensuring they matched the format expected by the `UserManager.validate_user` method. 
2.  Refactored the code where the user keys were extracted from the API requests to use this new utility function.
##  Extensions and detail:
1.  **Moderator Management**
-   Endpoint: `/create_moderator`
-   Description: This endpoint allows the creation of moderator accounts. It requires an `Admin-Key` in the request header for authorization.
-   Test: Verified that only users with the correct `Admin-Key` could create moderators and that the moderators were assigned unique moderator keys.
2.  **Post Editing**
-   Endpoint: `/post/<int:post_id>/edit`
-   Description: This endpoint enables users to edit their posts. It requires the user's ID and key for authentication.
-   Test: Checked that posts could only be edited by the user who created them, using the correct user ID and key.
3.  **User Profile Updates**   
-   Endpoint: `/user/<int:user_id>/update`
-   Description: This endpoint allows users to update their profile information, including their real name.
-   Test: Ensured that profile updates were correctly saved and that users could only update their own profiles.
4.  **Post Search by Keyword**    
-   Endpoint: `/posts/search`
-   Description: This endpoint provides a search functionality to find posts containing specific keywords.
-   Test: Verified that the endpoint returned all posts containing the given keyword.
5.  **User Ban System**
-   Endpoint: `/ban_user/<int:user_id>`
-   Description: This endpoint allows moderators to ban users. It requires a moderator key for authorization.
-   Test: Tested that only moderators could ban users and that banned users could no longer create posts.