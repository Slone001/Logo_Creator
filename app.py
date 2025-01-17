from flask import Flask, render_template, request, redirect, url_for
import os
import data.website as website

app = website.create_app()


if __name__ == '__main__':
    website.check_folder_structure()
    app.run(debug=True)

