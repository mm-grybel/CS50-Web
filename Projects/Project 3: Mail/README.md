# Mail

A front-end for an email client that makes API calls to send and receive emails.

## API

The application supports the following API routes:

#### GET /emails/`<str:mailbox>`

Sending a GET request to `/emails/<mailbox>` where `<mailbox>` is either `inbox`, `sent`, or `archive` returns back to the user (in JSON form) a list of all emails in that mailbox, in reverse chronological order. For example, if the user sends a GET request to `/emails/inbox`, they get a JSON response like the below (representing two emails):
```json
[
    {
        "id": 100,
        "sender": "foo@example.com",
        "recipients": ["bar@example.com"],
        "subject": "Hello!",
        "body": "Hello, world!",
        "timestamp": "Jan 2 2020, 12:00 AM",
        "read": false,
        "archived": false
    },
    {
        "id": 95,
        "sender": "baz@example.com",
        "recipients": ["bar@example.com"],
        "subject": "Meeting Tomorrow",
        "body": "What time are we meeting?",
        "timestamp": "Jan 1 2020, 12:00 AM",
        "read": true,
        "archived": false
    }
]
```
Each email specifies its `id` (a unique identifier), a `sender` email address, an array of `recipients`, a string for `subject`, `body`, and `timestamp`, as well as two boolean values indicating whether the email has been `read` and whether the email has been `archived`.

In JavaScript, we can use fetch to make a web request. Therefore, the following JavaScript code
```javascript
fetch('/emails/inbox')
.then(response => response.json())
.then(emails => {
    // Print emails
    console.log(emails);

    // ... do something else with emails ...
});
```
would make a GET request to `/emails/inbox`, convert the resulting response into JSON, and then provide the user with the array of emails inside the variable `emails`. We can print that value out to the browser’s console using `console.log` (if the user doesn't have any emails in their inbox, this will be an empty array), or do something else with that array.

If the user requests an invalid mailbox (anything other than `inbox`, `sent`, or `archive`), they instead get back the JSON response `{"error": "Invalid mailbox."}`.

#### GET /emails/`<int:email_id>`

Sending a GET request to `/emails/email_id` where `email_id` is an integer id for an email returns a JSON representation of the email, like the below:
```json
{
        "id": 100,
        "sender": "foo@example.com",
        "recipients": ["bar@example.com"],
        "subject": "Hello!",
        "body": "Hello, world!",
        "timestamp": "Jan 2 2020, 12:00 AM",
        "read": false,
        "archived": false
}
```
If the email doesn’t exist, or if the user does not have access to the email, the route instead returns a `404 Not Found error` with a JSON response of `{"error": "Email not found."}`.

To get email number 100, for example, we might write JavaScript code like
```javascript
fetch('/emails/100')
.then(response => response.json())
.then(email => {
    // Print email
    console.log(email);

    // ... do something else with email ...
});
```

#### POST /emails

To send an email, the user can send a POST request to the `/emails` route. The route requires three pieces of data to be submitted: a `recipients` value (a comma-separated string of all users to send an email to), a `subject` string, and a `body` string. For example, we could write JavaScript code like
```javascript
fetch('/emails', {
  method: 'POST',
  body: JSON.stringify({
      recipients: 'baz@example.com',
      subject: 'Meeting time',
      body: 'How about we meet tomorrow at 3pm?'
  })
})
.then(response => response.json())
.then(result => {
    // Print result
    console.log(result);
});
```
If the email is sent successfully, the route responds with a `201 status code` and a JSON response of `{"message": "Email sent successfully."}`.

There must be at least one email recipient: if one isn’t provided, the route instead responds with a `400 status code` and a JSON response of `{"error": "At least one recipient required."}`. All recipients must also be valid users who have registered on this particular web application: if the user tries to send an email to baz@example.com, but there is no user with that email address, they’ll get a JSON response of `{"error": "User with email baz@example.com does not exist."}`.

#### PUT /emails/`<int:email_id>`

This route provides the ability to mark an email as `read/unread` or as `archived/unarchived`. To do so, the user sends a PUT request (instead of a GET request) to `/emails/<email_id>` where `email_id` is the id of the email the user is trying to modify. For example, JavaScript code like
```javascript
fetch('/emails/100', {
  method: 'PUT',
  body: JSON.stringify({
      archived: true
  })
})
```
would mark email number 100 as archived.

## Specification

* **Send Mail**: When a user submits the email composition form, the JavaScript code actually sends the email.
    * A `POST` request to `/emails` is made, with values for `recipients`, `subject`, and `body` passed.
    * Once the email has been sent, the user’s `sent` mailbox is loaded.
* **Mailbox**: When a user visits their `Inbox`, `Sent mailbox`, or `Archive`, the appropriate mailbox is loaded.
    * A `GET` request to `/emails/<mailbox>` is made to request the emails for a particular mailbox.
    * When a mailbox is visited, the application first queries the API for the latest emails in that mailbox.
    * When a mailbox is visited, the name of the mailbox appears at the top of the page.
    * Each email is then rendered in its own box that displays who the email is from, what the subject line is, and the timestamp of the email.
    * If the email is unread, it appears with a white background. If the email has been read, it appears with a gray background.
* **View Email**: When a user clicks on an email, the user is taken to a view where they see the content of that email.
    * A `GET` request to `/emails/<email_id>` is made to request the email.
    * The application shows the email’s `sender`, `recipients`, `subject`, `timestamp`, and `body`.
    * Once the email has been clicked on, that email is marked as read. A `PUT` request to `/emails/<email_id>` is made to update whether an email has been read or not.
* **Archive and Unarchive**: The user can archive and unarchive emails that they have received.
    * When viewing an `Inbox` email, the user is presented with a button that lets them archive the email. When viewing an `Archive` email, the user is presented with a button that enables them to unarchive the email. This requirement does not apply to emails in the `Sent` mailbox.
    * A `PUT` request to `/emails/<email_id>` is made to mark an email as archived or unarchived.
    * Once an email has been archived or unarchived, the user’s `inbox` is loaded.
* **Reply**: The user can reply to an email.
    * When viewing an email, the user is presented with a “Reply” button that lets them reply to the email.
    * When the user clicks the “Reply” button, they are taken to the email composition form.
    * The composition form is pre-filled with the `recipient` field set to whoever sent the original email.
    * The `subject` line is pre-filled. If the original email had a subject line of `foo`, the new subject line would be `Re: foo`. (If the subject line already begins with `Re:`, no need to add it again.)
    * The `body` of the email is pre-filled with a line like `"On Jan 1 2020, 12:00 AM foo@example.com wrote:"` followed by the original text of the email.