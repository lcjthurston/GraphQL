from graphene import Schema, ObjectType, String, Int, Field


class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()


class Query(ObjectType):
    user = Field(UserType, user_id=Int())

    # dummy data store
    users = [
        {"id": 1, "name": "Andy Doe", "age": 33},
        {"id": 2, "name": "Andia Doe", "age": 34},
        {"id": 3, "name": "Julie Sullivan", "age": 31},
        {"id": 4, "name": "John Barber", "age": 29}
    ]

    @staticmethod
    def resolve_user(root, info, user_id):
        matched_users = [user for user in Query.users if user["id"] == user_id]
        return matched_users[0] if matched_users else None
    

# OOP aside
# - instance methods (first argument is self)
# - class methods (first argument is cls)
# - static methods (root, root_value, or source)

schema = Schema(query=Query)

gql = '''
query {
    user(userId: 4) {
        id
        name
        age    
    }
}
'''

if __name__ == "__main__":
    result = schema.execute(gql, root_value="some other data source")
    print(result)
