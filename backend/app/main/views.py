from flask import Flask, jsonify, request, abort, make_response
from . import main 


# Get all users
@main.route("/", methods=["GET"])
def index():
    return "Welcome to MoveUP SMS Sign-Up Tool!"
