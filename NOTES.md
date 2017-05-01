# Steps Performed

## Provisioning the EC2 instance

  1. EC2 nano instance was selected
  1. Role with RDS and S3 Read-Only permissions created for the EC2 instance
  1. 8GB of SSD GP2
  1. Launch

## Installing RapidSMS

  1. Installed `python35-virtualenv` (pulls in the other python packages), `git`
    * Might just be able to install virtual env and it will install the versions of python and pip required
  2. SSH confguration for the EC2 instance ([Instructions][])
    1. Create an RSA key `ssh-keygen -t rsa`
    2. Uplaod the public key to the IAM user
    3. Added the ssh configuration for the instance to clone from the AWS CodeCommit repo in `~/.ssh/config`
    4. Set the `~/.ssh/config` file to `600` file permissions
  3. Create a `virtualenv` with `python35`
  4. Install `Django` via `pip`
    * `pip install Django`
  5. Create RapidSMS project: 
    * `django-admin.py startproject --template=https://github.com/rapidsms/rapidsms-project-template/zipball/master --extension=py,rst SmsAlertSystem`
  6. Install dependencies: `pip install -r requirements/base.txt`

[Instructions]: http://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-ssh-unixes.html?icmpid=docs_acc_console_connect

# Useful Django Commands

  * Database commands:
    * `python manage.py syncdb`
    * `python manage.py makemigrations && python manage.py migrate`
  * Server commands
    * `python manage.py runserver`

## Improvements and Todos

  * Launch the instances into an ASG of 2 machines so that if one machines goes down, traffic and still be served
  * Use a CloudFormation template
