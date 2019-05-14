from flask import Flask, flash, request, redirect, url_for,render_template
import flask-uploads

@route('/',methods = ['GET'])
def default():
    return render_template('index.html')