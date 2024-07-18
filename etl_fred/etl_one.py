import http.client
import yaml
import json
import pandas as pd



db = yaml.safe_load(open('fred_key.yaml'))

import http.client

key = db['KEY']


conn = http.client.HTTPSConnection("api.stlouisfed.org")
payload = ''
headers = {
  'T179Yl9TaMdmP43fXF5N2d8IfesSGRKiTRxNrSqu': 'T179Yl9TaMdmP43fXF5N2d8IfesSGRKiTRxNrSqu',
  'Cookie': 'ak_bmsc=81B1FC46D5DD7964D12064DA7D9FAE4A~000000000000000000000000000000~YAAQDVLIF36xDk+QAQAAT9K1UBjVlcjW3u6vRGobP3sjw40dIsC/URHS16Px+PGaJStl2D5r0L7o2hDsPt5Pz0KXPrICICuan15QRLiEfJUEkZ1+GR0YdTsEdR669H/Yi54rdNZkT0q3HXaQkGJPmTjqfc8ziln05JU6h+xUcwKll67QVRWO1h5UWwoIBupBN4Ziju5wy09VhGBr+BH60dXq/H+TH2FZ5JTURXdJUk0t37JqIxp29OPpp0GgE5rHvklKcWBO3OBhgGklPO1AjqnBJ2L/4ccrkHZ/ADdSgOxw6CJoGDNrJc38aZIZwOe5D7ZlFArBSpDNhFUR6HkhLi0EHYMBa16YkVzuJ19wykoVtbv7doQd5IpkDhYruFIbAWU=; bm_sv=1FF63F607427ECDA49F70A3815D33870~YAAQDVLIF9HPDk+QAQAApLi2UBjpyMAsnoDQQ4if7ItuW2EA9NYjcxaB+mfybUeBD+mtrOaCVQfMSm6V5eYquAf1XPxxaSHWaVFzPKAo1l8MnjDqQuCAkGtsVBcZXh7jF97Rldg+eRaeiUdcpNt6ZO6cijQ9VUq44gqrVyU3nJqAotWHJL0HJW8TmX7996+8SWNlprFALLjrSs2vdIL81QG/cNe7IaErO/fMOo5gRaNtryk7ekxf0j9yNk3fZZjupkkR/g==~1; cookiesession1=678A3E1FD87BEEDA6FC19092D934FF42'
}
conn.request("GET", f"/fred/series/observations?series_id=GFDEBTN&api_key={key}&file_type=json", payload, headers)
res = conn.getresponse()
data = res.read()



df = pd.DataFrame(json.loads(data.decode("utf-8")))

print(df.columns)


