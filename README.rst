Sms Alert System
========================

.. image:: https://travis-ci.org/ColectivaLegal/SmsAlertSystem.svg?branch=master
    :target: https://travis-ci.org/ColectivaLegal/SmsAlertSystem

Below you will find basic setup instructions for the ``SmsAlertSystem`` project. To begin you should have the following
applications installed on your local development system:

- `Python >= 3.4 <http://www.python.org/getit/>`_
- `pip >= 7.0.3 <http://www.pip-installer.org/>`_
- `virtualenv >= 13.0.3 <http://www.virtualenv.org/>`_

Python 3.4 is specifically requred because that is the version of python used for the `AWS Elastic Beanstalk stack`__.

__ https://aws.amazon.com/elasticbeanstalk/


Getting Started: Running Locally
--------------------------------

To setup your local environment you should create a virtualenv and install the
necessary requirements::

    virtualenv SmsAlertSystem-env

On Posix systems you can activate your environment like this::

    source SmsAlertSystem-env/bin/activate

On Windows, you'd use::

    SmsAlertSystem-env\Scripts\activate

Then::

    cd SmsAlertSystem
    pip install -U -r requirements.txt

The ``SmsAlertSystem`` project uses Twilio to send and receive text messages. You will need to set environment variables
which define the account security identifier, authorization token, associated phone number, and host. The phone number
should have the format ``(###) ###-####``. When running locally, the host will be ``localhost:8000``. The port number is
not necessary if the server is running on port 80.::

    export RSMS_ACCOUNT_SID="..."
    export RSMS_AUTH_TOKEN="..."
    export RSMS_NUMBER="..."
    export RSMS_HOST="..."

Create the local database::

    python manage.py makemigrations
    python manage.py migrate

You should now be able to run the development server::

    python manage.py runserver


Sending Messages to the Local Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Create a *python* script that allows the user to send messages to the local server.


Deploying to Elastic Beanstalk
------------------------------

One Time Set-Up
~~~~~~~~~~~~~~~

An EB project is initialized locally and an environment in EB is created via::

    eb init colectiva
    eb create rapidsms-alert-sys-env
    # this should print the environment that was just created
    eb list

There is a circular dependency where Twilio needs to know the CNAME on both the RapidSMS instance and in the Twilio
console. However, this name is not created until the instance is deployed. Thus, first, the EB application will be
deployed to get the CNAME and then we'll update the environment variables and Twilio configuration::

    eb deploy

Grab the CNAME of the host via (this will only work after the CNAME has been created, may have to wait a minute or
two)::

    eb status | grep CNAME

The next steps is to configure Twilio:
    #. Open the Twilio console
    #. Purchase a phone number
    #. Go to ``Phone Numbers``, which is found on the left side navigation bar
    #. Click the purchased phone number
    #. In the ``Messaging`` section, set the following if necessary
         * *Configure With*: Webhooks, or TwiML Bins or Functions
         * *A Message Comes In*: Webhook, ``http://${CNAME}/backend/twilio/``, HTTP POST
         * The *Primary Handler Fails* value should be blank
    #. Don't forget to click ``Save``

The environment variables needed by the application need to be defined in the EB environment as was done when running
the application locally `(eb setenv)`_::

    eb setenv RSMS_ACCOUNT_SID="..." \
              RSMS_AUTH_TOKEN="..." \
              RSMS_NUMBER="..." \
              RSMS_HOST="..."
    # after this completed, use the following to print the environment
    eb printenv

.. _(eb setenv): http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb3-setenv.html

Updating the EB Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~

After making code changes, the changes must be committed to the local git repository. The EB application can then be
updated via::

    eb deploy

There are a number of commands that are useful, post-deployment::

    # open the RapidSMS webpage
    eb open
    # ssh into the ec2 instance
    eb ssh

If statistics about the application is desired, then the ``eb appversion`` provides a simple interface for obtaining
it. The deployment on the EC2 host is located at ``/opt/python/current/``.

Sending Messages to the Remote Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Create a *python* script that allows the user to send messages to the remote server.

Restarting The Remote Server on the Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

EBS uses Apache as the serving engine. To restart it, run the following::

    apachectl -k restart

This is based on the (`Apache Documentation`_).

.. _Apache Documentation: https://httpd.apache.org/docs/2.4/stopping.html

References
==========

* `RapidSMS`_: The framework the SMS system is built on top of, which itself is built on top of Django
* `Rhythm CSS`_: CSS used in the restview script

.. _RapidSMS: https://www.rapidsms.org/
.. _Rhythm CSS: https://github.com/Rykka/rhythm.css
