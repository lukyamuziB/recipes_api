from flask_restplus import reqparse

pagination_args= reqparse.RequestParser()
pagination_args.add_argument('q', type= str, required = False, help = 'Query recipe or categories')
pagination_args.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_args.add_argument('per_page', type=int, required=False, choices=[2, 10, 20, 30, 40, 50],
                                  default=10, help='Results per page {error_msg}')
