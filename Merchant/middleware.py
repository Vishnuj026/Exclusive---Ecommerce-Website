from django.utils.deprecation import MiddlewareMixin
from geoip2 import database
from ipware import get_client_ip

class CurrencyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        client_ip, _ = get_client_ip(request)
        print(f"Detected IP Address: {client_ip}")  # Debug statement
        
        # Use 'GeoLite2-Country.mmdb' and access the country information
        with database.Reader('GeoLite2-Country.mmdb') as reader:
            try:
                response = reader.country(client_ip)  # Use 'country' instead of 'city'
                country_code = response.country.iso_code
                print(f"Detected Country Code: {country_code}")  # Debug statement
            except Exception as e:
                print(f"GeoIP2 Exception: {e}")  # Debug statement
                country_code = 'US'  # Default to IN if there's an error

        # Set the currency based on the country code
        if country_code == 'IN':
            request.currency = '₹'
        else:
            request.currency = '$'
