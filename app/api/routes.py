from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/hello')
def getdata():
    return {'hi': 'hello'}


@api.route('/library', methods = ['POST'])
@token_required
def create_book(current_user_token):
    title = request.json['title']
    author = request.json['author']
    length = request.json['length']
    type = request.json['type']
    token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(title, author, length, type, token = token )

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books', methods = ['GET'])
@token_required
def get_book(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(token = a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)  



@api.route('/books/<id>', methods = ['POST', 'PUT'])
@token_required
def update_book(current_user_token, id):
    book = Book.query.get(id)
    book.email = request.json['email']
    book.phone_number = request.json['phone_number']
    book.address = request.json['address']
    book.token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)


@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema(book)
    return jsonify(response)