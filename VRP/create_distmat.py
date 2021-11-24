import requests
import pandas as pd

data=pd.read_excel("data_1.xlsx",engine='openpyxl')

node_mother=data.query('Category=="Mother"').reset_index(drop=True)
node_daughter=data.query('Category=="Daughter"').reset_index(drop=True)

node_list = [*node_mother.center_name.values]
DC = [*node_daughter.center_name.values]
node_list.extend(DC)
dc_list = node_list
dist_matrix = {i:{j:0 for j in dc_list} for i in dc_list}
time_matrix = {i:{j:0 for j in dc_list} for i in dc_list}

n=0
for i in dc_list:
    origin = (data.loc[data.center_name==i,'latitude'].values[0],data.loc[data.center_name==i,'longitude'].values[0])
    print('main= ',n)
    n=n+1
    for j in dc_list:
        try:
            k=0
            destination =(data.loc[data.center_name==j,'latitude'].values[0],data.loc[data.center_name==j,'longitude'].values[0])
            # if self.USE_GOOGLE_API is True:
            #     distance = (self.gmaps.distance_matrix(origin, destination, mode='driving', avoid='ferries')['rows'][0]['elements'][0]['distance']['value'])/1000
            #     time = (self.gmaps.distance_matrix(origin, destination, mode='driving', avoid='ferries')['rows'][0]['elements'][0]['duration']['value'])/3600
            # if distance>self.model_parameters['MAX_DISTANCE']:
            #     print(f'Warning!!! Distance between {i} and {j} seems high')
            # time_matrix[i][j] = time
            # OSRM
            source_cord = str(origin[1])+','+str(origin[0])
            destination_cord = str(destination[1])+','+str(destination[0])
            # url = 'http://router.project-osrm.org/route/v1/driving/'+source_cord+';'+destination_cord+'?steps=true'
            url=  'http://router.project-osrm.org/route/v1/driving/{0};{1}?steps=true'.format(source_cord,destination_cord)
            req = requests.get(url)
            response = req.json()
            distance = response['routes'][0]['legs'][0]['distance']/1000
            time= response['routes'][0]['legs'][0]['duration']/3600
            # print(distance)
            dist_matrix[i][j] = distance
            time_matrix[i][j]=time
            print(n if n%2==0)        
        except:
            print(f'Could not compute distance for {j}')
print('Distance computation done...')


results_distance = pd.DataFrame(dist_matrix, index = dist_matrix.keys(), columns = dist_matrix.keys())
results_distance.to_csv('dist_matrix_df.csv',index=False)

results_time = pd.DataFrame(time_matrix, index = time_matrix.keys(), columns = time_matrix.keys())
results_time.to_csv('time_matrix_df.csv',index=False)