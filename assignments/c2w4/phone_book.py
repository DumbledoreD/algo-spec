class Query:
    def __init__(self, query):
        self.type = query[0]
        self.number = int(query[1])
        if self.type == "add":
            self.name = query[2]


class PhoneBook:
    def __init__(self, size):
        self.names = [None] * size

    def add(self, number, name):
        self.names[number] = name

    def remove(self, number):
        self.names[number] = None

    def find(self, number):
        return self.names[number]


def process_queries(queries):
    results = []

    phone_book = PhoneBook(10 ** 7)

    for query in queries:

        if query.type == "add":
            phone_book.add(query.number, query.name)

        elif query.type == "del":
            phone_book.remove(query.number)

        elif query.type == "find":
            results.append(phone_book.find(query.number) or "not found")

    return results


def read_queries():
    n = int(input())
    return [Query(input().split()) for i in range(n)]


def write_responses(results):
    print("\n".join(results))


if __name__ == "__main__":
    write_responses(process_queries(read_queries()))
