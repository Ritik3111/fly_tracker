# fly_tracker
An open source project that helps you get the best flight deals!

![license](https://img.shields.io/github/license/Ritik3111/fly_tracker)
![issues](https://img.shields.io/github/issues/Ritik3111/fly_tracker)
![status](https://img.shields.io/github/actions/workflow/status/Ritik3111/fly_tracker/setup.yml)
[![docs](https://img.shields.io/readthedocs/fly-tracker)](https://fly-tracker.readthedocs.io/en/latest/)
[![PyPI](https://img.shields.io/pypi/v/fly-tracker)](https://pypi.org/project/fly-tracker/)
## Code Coverage

[![codecov](https://codecov.io/gh/Ritik3111/fly_tracker/branch/main/graph/badge.svg)](https://codecov.io/gh/Ritik3111/fly_tracker)
## Overview

The Fly Tracker library lets you monitor the flight prices for any route.
The user has the option to set up notifications for the tracked route which can help him book tickets when he/she wants to. Once you run the command(mentioned in [Usage]#Usage) to start the notifications, the script runs at 12 AM and 12 PM Everyday and this is exactly when you receive the email.
The source of our data is Google Flights, which is very reliable since it lists the best price for every option and
hence, we notify you with all options avalaible to you. 

## Table of Contents

- [Installation](#Installation)
- [Usage](#Usage)
- [Example](#Example)

## Installation 

To install the library: 

`pip install fly_tracker`

## Usage

The library takes the following arguments:

| Argument | Name | Type | Description
| -------- | -------- | -------- | -------- |
| src | Source | string | Source City |
| dst | Destination | string |Destination City |
| price | Price | int |The threshold price that you want to set |
| date | Date | string | The date you want to fly on |
| email | Email Address | string | The email address where you want to receive the notifications |

Run the following command:
`python flytracker --src < src-city > --dest < dest-city > --price < price > --date < date > --email < email >`

Replace < src-city >, < dest-city >, < price >, < date > and < email > with your desired values. This will start tracking the flight prices for the specified route.

## Example
To receive notifications regarding fares below $100 for the New York to Boston route on May 12th, please execute the following command, with the specified email address included:

`python flytracker --src "New York" --dest "Boston" --price 100 --date "12th May" --email "pandaritik39@gmail.com"`