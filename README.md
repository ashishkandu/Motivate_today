# Motivational quotes everyday

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## About <a name = "about"></a>

A small project to send email daily from python using the built in smtplib package.
The email consist of a motivational quote fetched from a public API.

## Getting Started <a name = "getting_started"></a>

Preety simple to use, enter your email, password in credentials.json and update the recipients emails.

### Prerequisites

To use this program, create a file named "credentials.json" and give your credentials in below format. By default index 1 item is choosen. This can be changed by changing variable *entry* in code. Corresponding host needs to be used as per email provider.

```json
[
    {
        "email": "email@gmail.com",
        "password": "app_password"
    },
    {
        "email": "email@yahoo.com",
        "password": "app_password"
    }

]
```


## Usage <a name = "usage"></a>

Deploy the program as task in the cloud and get daily motivational quotes.
