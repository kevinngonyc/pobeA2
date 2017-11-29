from flask import jsonify
from flask import request
from app import app, db, base

@app.route('/kanban/boards', methods=['POST'])
def createBoard():

	b = base.Board(title=request.args.get('title'))
	db.session.add(b)
	db.session.commit()

	b_schema = base.BoardSchema()
	bJSON = b_schema.dump(b).data
	bJSON["board_elements"] = [];

	return jsonify({
	  	"success": True,
	  	"data": {
	    	"board": bJSON
  		}
	})

@app.route('/kanban/boards', methods=['DELETE'])
def deleteBoard():

	b = base.Board.query.get(request.args.get('id'))

	db.session.delete(b)
	db.session.commit()

	return jsonify({
	  	"success": True
	})

@app.route('/kanban/boards', methods=['GET'])
def getBoards():

	b = base.Board.query.all()

	boards = []
	for board in b:

		todo = base.Element.query.filter_by(category='todo', board_id=board.id).all()
		inprogress = base.Element.query.filter_by(category='inprogress', board_id=board.id).all()
		done = base.Element.query.filter_by(category='done', board_id=board.id).all()

		board_schema = base.BoardSchema()
		bJSON = board_schema.dump(board).data
		bJSON["todo_count"] = len(todo)
		bJSON["inprogress_count"] = len(inprogress)
		bJSON["done_count"] = len(done)

		boards.append(bJSON)

	return jsonify({
	  "success": True,
	  "data": {
	    "boards": boards
	  }
	})

@app.route('/kanban/boards/<int:board_id>', methods=['GET'])
def getBoard(board_id):
	b = base.Board.query.get(board_id)

	todo = base.Element.query.filter_by(category='todo', board_id=board_id).all()
	inprogress = base.Element.query.filter_by(category='inprogress', board_id=board_id).all()
	done = base.Element.query.filter_by(category='done', board_id=board_id).all()

	todos = []
	inprogresses = []
	dones = []

	for t in todo:
		todos.append(elementToDict(t))
	for i in inprogress:
		inprogresses.append(elementToDict(i))
	for d in done:
		dones.append(elementToDict(d))

	return jsonify({
	  "success": True,
	  "data": {
	    "board": {
	      "id": b.id,
	      "title": b.title,
	      "created_at": b.created_at,
	      "updated_at": b.updated_at,
	      "todo": todos,
	      "inprogress": inprogresses,
	      "done": dones
	    }
	  }
	})

@app.route('/kanban/board_elements', methods=['POST'])
def createElement():

	e = base.Element(board_id=request.args.get('board_id'), description=request.args.get('description'), category=request.args.get('category'))
	db.session.add(e)
	db.session.commit()

	return jsonify({
	  "success": True,
	  "data": {
	    "board_element": elementToDict(e)
	  }
	})

@app.route('/kanban/board_elements', methods=['DELETE'])
def deleteElement():

	e = base.Element.query.get(request.args.get('board_element_id'))

	db.session.delete(e)
	db.session.commit()

	return jsonify({
	  	"success": True
	})

@app.route('/kanban/board_elements/advance', methods=['POST'])
def advanceElement():


	e = base.Element.query.get(request.args.get('id'))

	if(e.category == "todo"):
		db.session.query(base.Element).filter_by(id=request.args.get('id')).update({"category": "inprogress"})
	elif(e.category == "inprogress"):
		db.session.query(base.Element).filter_by(id=request.args.get('id')).update({"category": "done"})

	db.session.commit()

	return jsonify({
	  	"success": True
	})

@app.route('/kanban/tags', methods=['POST'])
def addTag():
	t = base.Tag(name=request.args.get('name'))
	db.session.add(t)
	db.session.commit()

	t_schema = base.TagSchema()
	tJSON = t_schema.dump(t).data
	tJSON["board_elements"] = [];

	return jsonify({
	  	"success": True,
	  	"data": {
	    	"tag": tJSON
  		}
	})

@app.route('/kanban/tags', methods=['GET'])
def getTags():

	t = base.Tag.query.all()

	tags = []
	for tag in t:

		tagElements = base.TagElement.query.filter_by(tag_id=tag.id).all()
		elementIndexes = []

		for te in tagElements:
			elementIndexes.append(te.board_element_id)

		tag_schema = base.TagSchema()
		tJSON = tag_schema.dump(tag).data
		tJSON["board_elements"] = elementIndexes

		tags.append(tJSON)


	return jsonify({
	  	"success": True,
	  	"data": {
	    	"tags": tags
		}
	})

@app.route('/kanban/tags/add', methods=['POST'])
def addTagToBoard():

	te = base.TagElement(board_element_id=request.args.get('board_element_id'), tag_id=request.args.get('tag_id'))
	db.session.add(te)
	db.session.commit()

	return jsonify({
	  	"success": True
	})

@app.route('/kanban/tags/add', methods=['DELETE'])
def delTagFromBoard():

	te = base.TagElement.query.filter_by(board_element_id=request.args.get('board_element_id'), tag_id=request.args.get('tag_id')).all()

	db.session.delete(te)
	db.session.commit()

	return jsonify({
	  	"success": True
	})

def elementToDict(e):
	et = base.TagElement.query.filter_by(board_element_id=e.id).all()

	tags = []
	for elementTag in et:

		tagElements = base.TagElement.query.filter_by(tag_id=elementTag.tag.id).all()
		elementIndexes = []

		for te in tagElements:
			elementIndexes.append(te.board_element_id)

		tag_schema = base.TagSchema()
		tJSON = tag_schema.dump(elementTag.tag).data
		tJSON["board_elements"] = elementIndexes

		tags.append(tJSON)

	return {
	      "id": e.id,
	      "board_id": e.board_id,
	      "category": e.category,
	      "created_at": e.created_at,
	      "updated_at": e.updated_at,
	      "description": e.description,
	      "tags": tags
	    }