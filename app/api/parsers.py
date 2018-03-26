from flask_restplus import reqparse

pagination_args= reqparse.RequestParser()
pagination_args.add_argument('q', type= str, required = False,
 location = 'args', help = 'Query recipe or categories')


pagination_args.add_argument('page', type=int, required=False,
 location = 'args', default=1, help='Page number')


pagination_args.add_argument('per_page', type=int, required=False,
 location = 'args', choices=[2,6, 10, 20, 30, 40, 50],
                    default=6, help='Results per page {error_msg}')
