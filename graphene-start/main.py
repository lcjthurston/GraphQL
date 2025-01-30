from graphene import Schema, ObjectType, String, Int, Field, List, Mutation


class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()


class CreateUser(Mutation):
    class Arguments:
        name = String()
        age = Int()

    user = Field(UserType)

    def mutate(self, info, name, age):
        user = {"id": len(Query.users) + 1, "name": name, "age": age}
        Query.users.append(user)
        return CreateUser(user=user)


class Query(ObjectType):
    user = Field(UserType, user_id=Int())
    users_by_min_age = List(UserType, min_age=Int())

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
    
    @staticmethod
    def resolve_users_by_min_age(root, info, min_age):
        return [user for user in Query.users if user["age"] >= min_age]


class Mutation(ObjectType):
    create_user = CreateUser.Field()

# OOP aside
# - instance methods (first argument is self)
# - class methods (first argument is cls)
# - static methods (root, root_value, or source)

schema = Schema(query=Query, mutation=Mutation)

gql_2 = '''
query {
    user(userId: 5) {
        name
        age    
    }
}
'''

# gql = '''
# query {
#     usersByMinAge(minAge: 30) {
#         id
#         name
#         age    
#     }
# }
# '''

gql = '''
mutation {
    createUser(name: "New User", age: 25) {
        user {
            id
            name
            age
        }    
    }
}
'''

if __name__ == "__main__":
    result = schema.execute(gql)
    print(result)
    result = schema.execute(gql_2)
    print(result)
