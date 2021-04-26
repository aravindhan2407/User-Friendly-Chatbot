from googleapiclient.discovery import build
my_api_key = "AIzaSyBdRoooTKL4BZNGGZXSY-rIiEtMSuh9QTU"
my_cse_id = "2efa4c9a84b9345ac"
 
def get_google_answer(search_term, api_key, cse_id, **kwargs):
   service = build("customsearch", "v1", developerKey=api_key)
   results = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
   content=results['items'][0]['htmlSnippet'].replace('\n',"")
   content= content.replace("<b>","")
   content= content.replace("</b>","")
   content= content.replace("<br>","")
   content= content.replace("&nbsp;...",".")
   return content