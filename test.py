# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import sqlalchemy as sa
# from website.models import User

# # an Engine, which the Session will use for connection
# # resources
# engine = create_engine('postgresql+psycopg2://scott:tiger@localhost/')

# Session = sessionmaker(engine)

# with Session() as session:
#     session.execute(sa.select().filter_by()).all()
#     # session.get(User, )

s = '''                <div class="col">
                    <div class="card">
                        <div class="card-body">
                            <h3 class="card-title">😃</h3>
                            <input type="radio" class="btn-check" name="emoji" value="{val}" id="emoji{val}" autocomplete="off">
                            <label class="btn btn-primary" for="emoji{val}">Happy</label>
                        </div>
                    </div>
                </div>
'''

for i in range(6):
    print(s.format(val=i))