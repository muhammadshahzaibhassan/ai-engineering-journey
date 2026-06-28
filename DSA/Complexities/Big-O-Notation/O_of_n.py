# the runtime or memory of an algorithm grows proportionally with the size of the input data
def find_paper(papers, name):
    for paper in papers:
        if paper == name:
            return True
    return False

papers = ['Ava', 'Emma', 'Jackson', 'Liam', 'Lucas', 'Mia', 'Noah', 'Oliver', 'Olivia', 'Sophia']

search_name = "Olivia"

result = find_paper(papers, search_name)

if result:
    print("Paper Found!")
else:
    print("Paper not found!")
