import requests


def moodle_login(username, password):
    url = "http://localhost/login/token.php"
    moodle_token = None
    params = {
        "username": username,     # or Moodle username
        "password": password,
        "service": "test",
    },
    moodle_response = requests.post(url, params=params)

    if moodle_response.status_code == 200:
        moodle_data = moodle_response.json()
        moodle_token = moodle_data.get("token")
        print(moodle_data)
    return moodle_token


def enroll_student(moodle_token, moodle_user_id, moodle_course_id):
    url = "http://localhost/webservice/rest/server.php"

    print("id: ", moodle_course_id, moodle_user_id)
    params = {
        "wstoken": moodle_token,
        "wsfunction": "enrol_manual_enrol_users",
        "moodlewsrestformat": "json",
        "enrolments[0][roleid]": 5,  # student role
        "enrolments[0][userid]": moodle_user_id,
        "enrolments[0][courseid]": moodle_course_id,
    }

    res = requests.post(url, params=params)
    # ---- PRINT DETAILS ----
    print("Status code:", res.status_code)
    print("Headers:", res.headers)
    print("Raw text:", res.text)

    try:
        print("JSON response:", res.json())
    except ValueError:
        print("Response is not JSON")

    # Raise error AFTER printing details
    res.raise_for_status()

    return True
