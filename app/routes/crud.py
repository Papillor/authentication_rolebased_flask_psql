from flask import render_template, request, redirect, url_for
from app import app
from app.__init__ import cur, conn

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages_num = int(request.form['pages_num'])
        review = request.form['review']
        cur.execute('INSERT INTO books (title, author, pages_num, review)'
                    'VALUES (%s, %s, %s, %s)',
                    (title, author, pages_num, review))
        conn.commit()
        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/edit/<int:book_id>/', methods=('GET', 'POST'))
def edit(book_id):
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages_num = int(request.form['pages_num'])
        review = request.form['review']
        cur.execute('UPDATE books SET title=%s, author=%s, pages_num=%s, review=%s WHERE id=%s',
                    (title, author, pages_num, review, book_id))
        conn.commit()
        return redirect(url_for('index'))

    cur.execute('SELECT * FROM books WHERE id = %s', (book_id,))
    book = cur.fetchone()

    return render_template('edit.html', book=book)

@app.route('/delete/<int:book_id>/', methods=['GET'])
def delete(book_id):
    if request.method == 'GET':
        cur.execute('DELETE FROM books WHERE id = %s', (book_id,))
        conn.commit()
        return redirect(url_for('index'))