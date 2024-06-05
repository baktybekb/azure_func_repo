import datetime
import logging
import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc).isoformat()
    logging.info(f'Timer triggered function ran at {utc_timestamp}')
    logging.info('=' * 100)
    logging.info('BAHAAAAAAA main.py file')

# import logging
# import datetime
# import azure.functions as func
#
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
#
# def main(mytimer: func.TimerRequest) -> None:
#     utc_timestamp = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc).isoformat()
#     if mytimer.past_due:
#         logging.info('The timer is past due!')
#     logging.info('Python timer trigger function ran at %s', utc_timestamp)
#     # Your existing code logic goes here
#     print('_' * 200)
#     logger.info('=' * 200)
#     print('BAHA')


# import logging
# import os
# import json
# from ldap3 import Server, Connection, Tls, ALL, SUBTREE
# from dotenv import load_dotenv
# import ssl
#
# load_dotenv()
#
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
#
# LDAP_URL = os.getenv('LDAP_URL')
# MANAGER_DN = os.getenv('MANAGER_DN')
# MANAGER_PASSWORD = os.getenv('MANAGER_PASSWORD')
# LDAP_SEARCH_BASE = os.getenv('LDAP_SEARCH_BASE')
# CONFIG_FILE_PATH = os.getenv('CONFIG_FILE_PATH')
#
# if not all([LDAP_URL, MANAGER_DN, MANAGER_PASSWORD, LDAP_SEARCH_BASE, CONFIG_FILE_PATH]):
#     logger.error("Missing environment variables. Ensure all required variables are set.")
#     raise ValueError("Missing environment variables.")
#
# with open(CONFIG_FILE_PATH, 'r') as config_file:
#     config = json.load(config_file)
#     GROUP_PATTERNS = config['group_patterns']
#
#
# class LDAPConnection:
#     def __init__(self, ldap_url, manager_dn, manager_password):
#         self.ldap_url = ldap_url
#         self.manager_dn = manager_dn
#         self.manager_password = manager_password
#         self.conn = None
#
#     def __enter__(self):
#         tls = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2)
#         self.conn = Connection(Server(self.ldap_url, use_ssl=True, tls=tls, get_info=ALL),
#                                user=self.manager_dn, password=self.manager_password, auto_bind=True)
#         logger.info("Connected to the LDAP server.")
#         return self.conn
#
#     def __exit__(self, exc_type, exc_value, traceback):
#         if self.conn:
#             self.conn.unbind()
#             logger.info("Disconnected from the LDAP server.")
#
#
# class LDAPService:
#     def __init__(self, connection):
#         self.connection = connection
#
#     def search_groups(self, search_base, group_patterns):
#         group_filter = "(|" + "".join([f"(cn={pattern})" for pattern in group_patterns]) + ")"
#         self.connection.search(search_base, group_filter, search_scope=SUBTREE, attributes=['member'])
#         return self.connection.entries
#
#     def search_users(self, search_base, user_dns, disabled_only=False):
#         if not user_dns:
#             return []
#
#         user_filter = "(|" + "".join([f"(distinguishedName={user_dn})" for user_dn in user_dns]) + ")"
#         if disabled_only:
#             user_filter = f"(&{user_filter}(userAccountControl:1.2.840.113556.1.4.803:=2))"
#         else:
#             user_filter = f"(&{user_filter}(!(userAccountControl:1.2.840.113556.1.4.803:=2)))"
#
#         self.connection.search(search_base, user_filter, search_scope=SUBTREE, attributes=['*'])
#         return self.connection.entries
#
#     def fetch_user_dns_by_groups(self, search_base, group_patterns):
#         groups = self.search_groups(search_base, group_patterns)
#         if not groups:
#             logger.info("No groups found with the specified patterns.")
#             return []
#
#         user_dns = set()
#         for group in groups:
#             user_dns.update(group['member'])
#
#         if not user_dns:
#             logger.info("No members found in the matching groups.")
#             return []
#
#         return user_dns
#
#
# class LDAPApplication:
#     def __init__(self, ldap_service):
#         self.ldap_service = ldap_service
#
#     def run(self, search_base, group_patterns):
#         logger.info("Fetching user DNs from groups...")
#         user_dns = self.ldap_service.fetch_user_dns_by_groups(search_base, group_patterns)
#
#         logger.info("Fetching users...")
#         active_users = self.ldap_service.search_users(search_base, user_dns)
#         if active_users:
#             pass  # sending active users to message queue
#         else:
#             logger.info("No user entries found.")
#
#         logger.info("Fetching disabled users...")
#         disabled_users = self.ldap_service.search_users(search_base, user_dns, disabled_only=True)
#         if disabled_users:
#             pass  # sending disabled users to message queue
#         else:
#             logger.info("No disabled user entries found.")
#
#         logger.info("LDAP Query Completed Successfully.")
#
#
# if __name__ == "__main__":
#     ldap_connection = LDAPConnection(LDAP_URL, MANAGER_DN, MANAGER_PASSWORD)
#     with ldap_connection as conn:
#         ldap_service = LDAPService(conn)
#         app = LDAPApplication(ldap_service)
#         app.run(LDAP_SEARCH_BASE, GROUP_PATTERNS)
