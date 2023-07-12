def UserEntity(data):
    return dict(id=data['_id'], name=data['name'], email=data['email'], password=data['password'])
