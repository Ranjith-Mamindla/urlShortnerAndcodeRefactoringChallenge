# CHANGES.md

##  Major Issues Identified

1. **Missing input validation**
   - User creation and update endpoints did not validate the email format or presence of required fields.
2. **Password storage**
   - Plain-text passwords were being stored, which is a security concern.
3. **Error handling**
   - Inconsistent or vague error responses for invalid user IDs or missing data.
4. **Duplicate user handling**
   - No check for duplicate emails during user creation.
5. **Thread safety**
   - Concurrent access to the in-memory store was not synchronized.

---

##  Changes Made

1. **Input Validation Added**
   - Email format and required fields are validated using a utility function.
2. **Hashed Passwords**
   - Passwords are now hashed using `werkzeug.security` before storage.
3. **Improved Error Handling**
   - Used consistent JSON error messages and HTTP status codes (e.g., 400 for bad requests, 404 for not found).
4. **Duplicate Email Check**
   - Added logic to prevent user creation with an already existing email.
5. **Thread Safety**
   - Used threading locks to prevent race conditions in the in-memory user store.

---

## Assumptions & Trade-offs

- **In-memory storage**: Assumed this was acceptable as per assignment instructions. No external DB used.
- **User ID type**: Used integers for user IDs and assumed autoincrement behavior.
- **Authentication**: Skipped login token/session management per the requirements.
- **No persistent storage**: Restarting the app clears user data — this was acceptable under constraints.

---

## ⏳ If I Had More Time

- Add email verification and password reset flows.
- Implement pagination for user listing.
- Use Marshmallow or Pydantic for schema validation.
- Add logging and metrics collection.
- Migrate to persistent DB (SQLite/Postgres) for real-world use.
