import webapp2
import cgi
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_username(username):
    return USER_RE.match(username)
def valid_password(password):
    return PASSWORD_RE.match(password)
def valid_email(email):
    return EMAIL_RE.match(email)

page_header = """
<!DOCTYPE html>
<html>
    <head>
        <title>signup</title>
        <style type="text/css">
            .error {
                color: red;
            }
        </style>
    </head>
    <body>
"""

page_footer = """
    </body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):

        signup_form = """
        <h1>Signup</h1>
            <form action="/" method="post">
                <table>
                    <tr>
                        <td><label for="username">Username</label></td>
                        <td>
                            <input name="username" type="text" value="" required>
                            <span class="error"></span>
                        </td>
                    </tr>
                    <tr>
                        <td><label for="password">Password</label></td>
                        <td>
                            <input name="password" type="password" required>
                            <span class="error"></span>
                        </td>
                    </tr>
                    <tr>
                        <td><label for"verify">Verify Password</label></td>
                        <td>
                            <input name="verify" type="password" required>
                            <span class="error"></span>
                        </td>
                    </tr>
                    <tr>
                        <td><label for="email">Email (optional)</label></td>
                        <td>
                            <input name="email" type="email" value="">
                            <span class="error"></span>
                        </td>
                    </tr>
                </table>
                <input type="submit">
            </form>
        """

        response = page_header + signup_form + page_footer
        self.response.write(response)

    def post(self):
        username = cgi.escape(self.request.get('username'), quote= True)
        password = cgi.escape(self.request.get('password'), quote= True)
        verify = cgi.escape(self.request.get('verify'), quote= True)
        email = cgi.escape(self.request.get('email'), quote= True)


        error_user = ""
        error_password = ""
        error_verify = ""
        error_email = ""

        if not valid_username(username):
            error_user= "That's not a valid username"

        if not valid_password(password):
            error_password= "That's not a valid password"
        elif password != verify:
            error_verify = "Passwords don't match"

        if not valid_email(email):
            error_email = "That's not a valid email"

        if error_user == "" and error_password == "" and error_verify == "" and error_email == "":
            self.redirect('/welcome?username={}'.format(username))
            return

        signup_form = """
        <h1>Signup</h1>
            <form action="/" method="post">
                <table>
                    <tr>
                        <td><label for="username">Username</label></td>
                        <td>
                            <input name="username" type="text" value="{0}" required>
                            <span class="error">{1}</span>
                        </td>
                    </tr>
                    <tr>
                        <td><label for="password">Password</label></td>
                        <td>
                            <input name="password" type="password" required>
                            <span class="error">{2}</span>
                        </td>
                    </tr>
                    <tr>
                        <td><label for"verify">Verify Password</label></td>
                        <td>
                            <input name="verify" type="password" required>
                            <span class="error">{3}</span>
                        </td>
                    </tr>
                    <tr>
                        <td><label for="email">Email (optional)</label></td>
                        <td>
                            <input name="email" type="email" value="{5}">
                            <span class="error">{4}</span>
                        </td>
                    </tr>
                </table>
                <input type="submit">
            </form>
        """.format(username, error_user, error_password, error_verify, error_email, email)

        response = page_header + signup_form + page_footer
        self.response.write(response)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            welcome_form = """
            <h1> Welcome, {}!!</h1>
            """.format(username)
            response = page_header + welcome_form + page_footer
            self.response.write(response)
        else:
            self.redirect('/')
            return


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
