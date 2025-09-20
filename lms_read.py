import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise Exception("Supabase URL or Key not found in environment variables!")

sb: Client = create_client(url, key)

# -----------------------
# Read Functions
# -----------------------

def list_books():
    """List all books with availability"""
    resp = sb.table("books").select("*").execute()
    books = resp.data
    for b in books:
        status = "Available" if b["stock"] > 0 else "Out of Stock"
        print(f'{b["book_id"]}: {b["title"]} by {b["author"]} ({status}, Stock: {b["stock"]})')

def search_books(keyword):
    """Search books by title, author, or category"""
    resp = (
        sb.table("books")
        .select("*")
        .or_(f"title.ilike.%{keyword}%,author.ilike.%{keyword}%,category.ilike.%{keyword}%")
        .execute()
    )
    results = resp.data
    if results:
        print("Search results:")
        for b in results:
            print(f'{b["book_id"]}: {b["title"]} by {b["author"]} (Category: {b["category"]}, Stock: {b["stock"]})')
    else:
        print("No books found.")

def member_details(member_id):
    """Show member details and their borrowed books"""
    # Get member info
    m_resp = sb.table("members").select("*").eq("member_id", member_id).execute()
    if not m_resp.data:
        print("Member not found!")
        return

    member = m_resp.data[0]
    print(f'Member: {member["name"]} ({member["email"]}) - Joined {member["join_date"]}')

    # Get borrowed books
    br_resp = (
        sb.table("borrow_records")
        .select("record_id, borrow_date, return_date, books(title, author)")
        .eq("member_id", member_id)
        .execute()
    )
    records = br_resp.data
    if records:
        print("\nBorrowed books:")
        for r in records:
            title = r["books"]["title"]
            author = r["books"]["author"]
            status = "Returned" if r["return_date"] else "Borrowed"
            print(f'- {title} by {author} ({status}, Borrowed on {r["borrow_date"]})')
    else:
        print("No borrow records for this member.")


if __name__ == "__main__":
    print("Library Management - Read Operations")
    print("1. List all books")
    print("2. Search books")
    print("3. Member details")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        list_books()
    elif choice == "2":
        keyword = input("Enter keyword (title/author/category): ").strip()
        search_books(keyword)
    elif choice == "3":
        member_id = int(input("Enter member_id: ").strip())
        member_details(member_id)
    else:
        print("Invalid choice!")
