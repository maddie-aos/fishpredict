eval_fut= pd.read_csv('results/DNN_performance/DNN_eval_future.txt', sep='\t', header=0)


#loading keras models: future
cit_sor_model_future = load_model('saved_models/Citharichthys_sordidus_future.h5')
eng_mor_model_future = load_model('saved_models/Engraulis_mordax_future.h5')
par_cal_model_future = load_model('saved_models/Paralichthys_californicus_future.h5')
sco_jap_model_future = load_model('saved_models/Paralichthys_californicus_future.h5')
thu_ala_model_future = load_model('saved_models/Thunnus_alalunga_future.h5')
xip_gla_model_future = load_model('saved_models/Xiphias_gladius_future.h5')

@app.route("/future")
def future():
    return render_template("future.html")


#Selecting Species in the Future
@app.route("/cit_sor_fut")
def cit_sor_fut():
    return render_template("cit_sor_fut.html")

@app.route("/eng_mor_fut")
def eng_mor_fut():
    return render_template("eng_mor_fut.html")

@app.route("/par_cal_fut")
def par_cal_fut():
    return render_template("par_cal_fut.html")

@app.route("/sco_jap_fut")
def sco_jap_fut():
    return render_template("sco_jap_fut.html")

@app.route("/thu_ala_fut")
def thu_ala_fut():
    return render_template("thu_ala_fut.html")

@app.route("/xip_gla_fut")
def xip_gla_fut():
    return render_template("xip_gla_fut.html")


#Future Distributions Pages
@app.route("/cit_sor_fut_dist")
def cit_sor_fut__dist():
    return render_template("cit_sor_fut_dist.html")

@app.route("/eng_mor_fut_dist")
def eng_mor_fut_dist():
     return render_template("eng_mor_fut_dist.html")

@app.route("/par_cal_fut_dist")
def par_cal_fut_dist():
     return render_template("par_cal_fut_dist.html")

@app.route("/sco_jap_fut_dist")
def sco_jap_fut_dist():
     return render_template("sco_jap_fut_dist.html")

@app.route("/thu_ala_fut_dist")
def thu_ala_fut_dist():
     return render_template("thu_ala_fut_dist.html")

@app.route("/xip_gla_fut_dist")
def xip_gla_fut_dist():
    return render_template("xip_gla_fut_dist.html")


#Predictions: Future
@app.route("/cit_sor_fut_pred")
def cit_sor_fut_pred():
    return render_template("cit_sor_fut_pred.html")

@app.route("/cit_sor_fut_pred", methods = ['POST'])
def predict_csorf():
    #taking in user input, making a dataframe
    lat = request.form.get('latitudechange')
    latitude = float(lat)
    lon = request.form.get('longitudechange')
    longitude = float(lon)
    items = {"deci_lat": [latitude], "deci_lon": [longitude]}
    df = pd.DataFrame(items)

    df = df[ (df['deci_lat']< 90.) & (df['deci_lat'] > -90.)]
    df = df[ (df['deci_lon']< 180.) & (df['deci_lon'] > -180.) ]

    if not df.empty:
        inRas=gdal.Open('stacked_bio_oracle_future/bio_oracle_future_stacked.tif')
        myarray=inRas.ReadAsArray()

        len_pd=np.arange(len(df))
        lon=df["deci_lon"]
        lat=df["deci_lat"]
        lon=lon.values
        lat=lat.values

        row=[]
        col=[]

        src=rasterio.open('stacked_bio_oracle_future/bio_oracle_future_stacked.tif', crs= 'espg: 4326')
        
        for i in len_pd:
            row_n, col_n = src.index(lon[i], lat[i])# spatial --> image coordinates
            row.append(row_n)
            col.append(col_n)
        
        mean_std=pd.read_csv('stacked_bio_oracle_future/future_env_bio_mean_std.txt',sep="\t")
        mean_std=mean_std.to_numpy()
        
        X=[]
        for j in range(0,9):
            print(j)
            band=myarray[j]
            x=[]
            
            for i in range(0,len(row)):
                value= band[row[i],col[i]]
                if value <-1000:
                    value=np.nan
                    x.append(value)
                else:
                    value = ((value - mean_std.item((j,1))) / mean_std.item((j,2))) # scale values
                    x.append(value)
            X.append(x)
        
        X.append(row)
        X.append(col)
        
        X =np.array([np.array(xi) for xi in X])
        
        df=pd.DataFrame(X)
        df=df.T
        
        df=df.dropna(axis=0, how='any')

        if not df.empty:
            input_X=df.loc[:,0:8]
            row=df[9]
            col=df[10]
            
            row_col=pd.DataFrame({"row":row,"col":col})
            
            input_X=input_X.values
            
            row=row.values
            col=col.values
            
            prediction_array=np.save('predictions/csor_future_prediction_array.npy',input_X)
            prediction_pandas=row_col.to_csv('predictions/csor__future_prediction_row_col.csv')
            
            input_X=np.load('predictions/csor_future_prediction_array.npy')
            df=pd.DataFrame(input_X)
            
            new_band=myarray[1].copy()
            new_band.shape
            
            new_values = cit_sor_model_future.predict(x=input_X,verbose=0) ###predict output value
            new_band_values=[]
            
            for i in new_values:
                new_value=i[1]
                new_band_values.append(new_value)
            new_band_values=np.array(new_band_values)
            resultdf = pd.DataFrame(new_band_values, columns=['predicted_result'])
            val = resultdf['predicted_result'].values[0]   
            val = val*100
            vals = str(val)

            result = "Likeliood of presence: " + vals + "%"

            map = folium.Map(location=[latitude, longitude],zoom_start=8, tooltip = 'This tooltip will appear on hover')
            folium.Marker(location=[latitude,longitude], tooltip=result).add_to(map)
            map.save(outfile='templates/csorf_map.html')

            return render_template('csorf_map.html')


            #return map._repr_html_()
        else: 
            return render_template('land_coord.html')
    else:
        return render_template('invalid.html')

@app.route("/eng_mor_fut_pred")
def eng_mor_fut_pred():
    return render_template("eng_mor_fut_pred.html")

@app.route("/eng_mor_fut_pred", methods = ['POST'])
def predict_emorf():
    #taking in user input, making a dataframe
    lat = request.form.get('latitudechange')
    latitude = float(lat)
    lon = request.form.get('longitudechange')
    longitude = float(lon)
    items = {"deci_lat": [latitude], "deci_lon": [longitude]}
    df = pd.DataFrame(items)

    df = df[ (df['deci_lat']< 90.) & (df['deci_lat'] > -90.)]
    df = df[ (df['deci_lon']< 180.) & (df['deci_lon'] > -180.) ]

    if not df.empty:
        inRas=gdal.Open('stacked_bio_oracle_future/bio_oracle_future_stacked.tif')
        myarray=inRas.ReadAsArray()

        len_pd=np.arange(len(df))
        lon=df["deci_lon"]
        lat=df["deci_lat"]
        lon=lon.values
        lat=lat.values

        row=[]
        col=[]

        src=rasterio.open('stacked_bio_oracle_future/bio_oracle_future_stacked.tif', crs= 'espg: 4326')
        
        for i in len_pd:
            row_n, col_n = src.index(lon[i], lat[i])# spatial --> image coordinates
            row.append(row_n)
            col.append(col_n)
        
        mean_std=pd.read_csv('stacked_bio_oracle_future/future_env_bio_mean_std.txt',sep="\t")
        mean_std=mean_std.to_numpy()
        
        X=[]
        for j in range(0,9):
            print(j)
            band=myarray[j]
            x=[]
            
            for i in range(0,len(row)):
                value= band[row[i],col[i]]
                if value <-1000:
                    value=np.nan
                    x.append(value)
                else:
                    value = ((value - mean_std.item((j,1))) / mean_std.item((j,2))) # scale values
                    x.append(value)
            X.append(x)
        
        X.append(row)
        X.append(col)
        
        X =np.array([np.array(xi) for xi in X])
        
        df=pd.DataFrame(X)
        df=df.T
        
        df=df.dropna(axis=0, how='any')

        if not df.empty:
            input_X=df.loc[:,0:8]
            row=df[9]
            col=df[10]
            
            row_col=pd.DataFrame({"row":row,"col":col})
            
            input_X=input_X.values
            
            row=row.values
            col=col.values
            
            prediction_array=np.save('predictions/emor_future_prediction_array.npy',input_X)
            prediction_pandas=row_col.to_csv('predictions/emor__future_prediction_row_col.csv')
            
            input_X=np.load('predictions/emor_future_prediction_array.npy')
            df=pd.DataFrame(input_X)
            
            new_band=myarray[1].copy()
            new_band.shape
            
            new_values = eng_mor_model_future.predict(x=input_X,verbose=0) ###predict output value
            new_band_values=[]
            
            for i in new_values:
                new_value=i[1]
                new_band_values.append(new_value)
            new_band_values=np.array(new_band_values)
            resultdf = pd.DataFrame(new_band_values, columns=['predicted_result'])
            val = resultdf['predicted_result'].values[0]   
            val = val*100
            vals = str(val)

            result = "Likeliood of presence: " + vals + "%"

            map = folium.Map(location=[latitude, longitude],zoom_start=8, tooltip = 'This tooltip will appear on hover')
            folium.Marker(location=[latitude,longitude], tooltip=result).add_to(map)
            map.save(outfile='templates/emorf_map.html')

            return render_template('emorf_map.html')
            #return map._repr_html_()

        else: 
            return render_template('land_coord.html')
    else:
        return render_template('invalid.html')

@app.route("/par_cal_fut_pred")
def par_cal__fut_pred():
    return render_template("par_cal_fut_pred.html")

@app.route("/par_cal_fut_pred", methods = ['POST'])
def predict_pcalf():
    #taking in user input, making a dataframe
    lat = request.form.get('latitudechange')
    latitude = float(lat)
    lon = request.form.get('longitudechange')
    longitude = float(lon)
    items = {"deci_lat": [latitude], "deci_lon": [longitude]}
    df = pd.DataFrame(items)

    df = df[ (df['deci_lat']< 90.) & (df['deci_lat'] > -90.)]
    df = df[ (df['deci_lon']< 180.) & (df['deci_lon'] > -180.) ]


    if not df.empty:
        inRas=gdal.Open('stacked_bio_oracle_future/bio_oracle_future_stacked.tif')
        myarray=inRas.ReadAsArray()

        len_pd=np.arange(len(df))
        lon=df["deci_lon"]
        lat=df["deci_lat"]
        lon=lon.values
        lat=lat.values

        row=[]
        col=[]

        src=rasterio.open('stacked_bio_oracle_future/bio_oracle_future_stacked.tif', crs= 'espg: 4326')
        
        for i in len_pd:
            row_n, col_n = src.index(lon[i], lat[i])# spatial --> image coordinates
            row.append(row_n)
            col.append(col_n)
        
        mean_std=pd.read_csv('stacked_bio_oracle_future/future_env_bio_mean_std.txt',sep="\t")
        mean_std=mean_std.to_numpy()
        
        X=[]
        for j in range(0,9):
            print(j)
            band=myarray[j]
            x=[]
            
            for i in range(0,len(row)):
                value= band[row[i],col[i]]
                if value <-1000:
                    value=np.nan
                    x.append(value)
                else:
                    value = ((value - mean_std.item((j,1))) / mean_std.item((j,2))) # scale values
                    x.append(value)
            X.append(x)
        
        X.append(row)
        X.append(col)
        
        X =np.array([np.array(xi) for xi in X])
        
        df=pd.DataFrame(X)
        df=df.T
        
        df=df.dropna(axis=0, how='any')

        if not df.empty:
            input_X=df.loc[:,0:8]
            row=df[9]
            col=df[10]
            
            row_col=pd.DataFrame({"row":row,"col":col})
            
            input_X=input_X.values
            
            row=row.values
            col=col.values
            
            prediction_array=np.save('predictions/pcal_future_prediction_array.npy',input_X)
            prediction_pandas=row_col.to_csv('predictions/pcal__future_prediction_row_col.csv')
            
            input_X=np.load('predictions/pcal_future_prediction_array.npy')
            df=pd.DataFrame(input_X)
            
            new_band=myarray[1].copy()
            new_band.shape
            
            new_values = par_cal_model_future.predict(x=input_X,verbose=0) ###predict output value
            new_band_values=[]
            
            for i in new_values:
                new_value=i[1]
                new_band_values.append(new_value)
            new_band_values=np.array(new_band_values)
            resultdf = pd.DataFrame(new_band_values, columns=['predicted_result'])
            val = resultdf['predicted_result'].values[0]   
            val = val*100
            vals = str(val)

            result = "Likeliood of presence: " + vals + "%"

            map = folium.Map(location=[latitude, longitude],zoom_start=8, tooltip = 'This tooltip will appear on hover')
            folium.Marker(location=[latitude,longitude], tooltip=result).add_to(map)
            map.save(outfile='templates/pcalf_map.html')
            return render_template('pcalf_map.html')
            #return map._repr_html_()
        else: 
            return render_template('land_coord.html')
    else:
        return render_template('invalid.html')

@app.route("/sco_jap_fut_pred")
def sco_jap_fut_pred():
    return render_template("sco_jap_fut_pred.html")

@app.route("/sco_jap_fut_pred", methods = ['POST'])
def predict_sjapf():
    #taking in user input, making a dataframe
    lat = request.form.get('latitudechange')
    latitude = float(lat)
    lon = request.form.get('longitudechange')
    longitude = float(lon)
    items = {"deci_lat": [latitude], "deci_lon": [longitude]}
    df = pd.DataFrame(items)

    df = df[ (df['deci_lat']< 90.) & (df['deci_lat'] > -90.)]
    df = df[ (df['deci_lon']< 180.) & (df['deci_lon'] > -180.) ]

    if not df.empty:
        inRas=gdal.Open('stacked_bio_oracle_future/bio_oracle_future_stacked.tif')
        myarray=inRas.ReadAsArray()

        len_pd=np.arange(len(df))
        lon=df["deci_lon"]
        lat=df["deci_lat"]
        lon=lon.values
        lat=lat.values

        row=[]
        col=[]

        src=rasterio.open('stacked_bio_oracle_future/bio_oracle_future_stacked.tif', crs= 'espg: 4326')
        
        for i in len_pd:
            row_n, col_n = src.index(lon[i], lat[i])# spatial --> image coordinates
            row.append(row_n)
            col.append(col_n)
        
        mean_std=pd.read_csv('stacked_bio_oracle_future/future_env_bio_mean_std.txt',sep="\t")
        mean_std=mean_std.to_numpy()
        
        X=[]
        for j in range(0,9):
            print(j)
            band=myarray[j]
            x=[]
            
            for i in range(0,len(row)):
                value= band[row[i],col[i]]
                if value <-1000:
                    value=np.nan
                    x.append(value)
                else:
                    value = ((value - mean_std.item((j,1))) / mean_std.item((j,2))) # scale values
                    x.append(value)
            X.append(x)
        
        X.append(row)
        X.append(col)
        
        X =np.array([np.array(xi) for xi in X])
        
        df=pd.DataFrame(X)
        df=df.T
        df=df.dropna(axis=0, how='any')

        if not df.empty:
            input_X=df.loc[:,0:8]
            row=df[9]
            col=df[10]
            
            row_col=pd.DataFrame({"row":row,"col":col})
            
            input_X=input_X.values
            
            row=row.values
            col=col.values
            
            prediction_array=np.save('predictions/sjap_future_prediction_array.npy',input_X)
            prediction_pandas=row_col.to_csv('predictions/sjap__future_prediction_row_col.csv')
            
            input_X=np.load('predictions/sjap_future_prediction_array.npy')
            df=pd.DataFrame(input_X)
            
            new_band=myarray[1].copy()
            new_band.shape
            
            new_values = sco_jap_model_future.predict(x=input_X,verbose=0) ###predict output value
            new_band_values=[]
            
            for i in new_values:
                new_value=i[1]
                new_band_values.append(new_value)
            new_band_values=np.array(new_band_values)
            resultdf = pd.DataFrame(new_band_values, columns=['predicted_result'])
            val = resultdf['predicted_result'].values[0]   
            val = val*100
            vals = str(val)

            result = "Likeliood of presence: " + vals + "%"

            map = folium.Map(location=[latitude, longitude],zoom_start=8, tooltip = 'This tooltip will appear on hover')
            folium.Marker(location=[latitude,longitude], tooltip=result).add_to(map)
            map.save(outfile='templates/sjapf_map.html')

            return render_template('sjapf_map.html')
            #return map._repr_html_()

        else: 
            return render_template('land_coord.html')
    else:
        return render_template('invalid.html')

@app.route("/thu_ala_fut_pred")
def thu_ala_fut_pred():
    return render_template("thu_ala_fut_pred.html")

@app.route("/thu_ala_fut_pred", methods = ['POST'])
def predict_talaf():
    #taking in user input, making a dataframe
    #taking in user input, making a dataframe
    lat = request.form.get('latitudechange')
    latitude = float(lat)
    lon = request.form.get('longitudechange')
    longitude = float(lon)
    items = {"deci_lat": [latitude], "deci_lon": [longitude]}
    df = pd.DataFrame(items)

    df = df[ (df['deci_lat']< 90.) & (df['deci_lat'] > -90.)]
    df = df[ (df['deci_lon']< 180.) & (df['deci_lon'] > -180.) ]

    if not df.empty:
        inRas=gdal.Open('stacked_bio_oracle_future/bio_oracle_future_stacked.tif')
        myarray=inRas.ReadAsArray()

        len_pd=np.arange(len(df))
        lon=df["deci_lon"]
        lat=df["deci_lat"]
        lon=lon.values
        lat=lat.values

        row=[]
        col=[]

        src=rasterio.open('stacked_bio_oracle_future/bio_oracle_future_stacked.tif', crs= 'espg: 4326')
        
        for i in len_pd:
            row_n, col_n = src.index(lon[i], lat[i])# spatial --> image coordinates
            row.append(row_n)
            col.append(col_n)
        
        mean_std=pd.read_csv('stacked_bio_oracle_future/future_env_bio_mean_std.txt',sep="\t")
        mean_std=mean_std.to_numpy()
        
        X=[]
        for j in range(0,9):
            print(j)
            band=myarray[j]
            x=[]
            
            for i in range(0,len(row)):
                value= band[row[i],col[i]]
                if value <-1000:
                    value=np.nan
                    x.append(value)
                else:
                    value = ((value - mean_std.item((j,1))) / mean_std.item((j,2))) # scale values
                    x.append(value)
            X.append(x)
        
        X.append(row)
        X.append(col)
        
        X =np.array([np.array(xi) for xi in X])
        
        df=pd.DataFrame(X)
        df=df.T
        
        df=df.dropna(axis=0, how='any')

        if not df.empty:
            input_X=df.loc[:,0:8]
            row=df[9]
            col=df[10]
            
            row_col=pd.DataFrame({"row":row,"col":col})
            
            input_X=input_X.values
            
            row=row.values
            col=col.values
            
            prediction_array=np.save('predictions/tala_future_prediction_array.npy',input_X)
            prediction_pandas=row_col.to_csv('predictions/tala__future_prediction_row_col.csv')
            
            input_X=np.load('predictions/tala_future_prediction_array.npy')
            df=pd.DataFrame(input_X)
            
            new_band=myarray[1].copy()
            new_band.shape
            
            new_values = thu_ala_model_future.predict(x=input_X,verbose=0) ###predict output value
            new_band_values=[]
            
            for i in new_values:
                new_value=i[1]
                new_band_values.append(new_value)

            new_band_values=np.array(new_band_values)
            resultdf = pd.DataFrame(new_band_values, columns=['predicted_result'])
            val = resultdf['predicted_result'].values[0]   
            val = val*100
            vals = str(val)

            result = "Likeliood of presence: " + vals + "%"

            map = folium.Map(location=[latitude, longitude],zoom_start=8, tooltip = 'This tooltip will appear on hover')
            folium.Marker(location=[latitude,longitude], tooltip=result).add_to(map)
            map.save(outfile='templates/talaf_map.html')

            return render_template('talaf_map.html')

            #return map._repr_html_()


        else: 
            return render_template('land_coord.html')
    else:
        return render_template('invalid.html')
    

@app.route("/xip_gla_fut_pred")
def xip_gla_fut_pred():
    return render_template("xip_gla_fut_pred.html")

@app.route("/xip_gla_fut_pred", methods = ['POST'])
def predict_xglaf():
    #taking in user input, making a dataframe
    lat = request.form.get('latitudechange')
    latitude = float(lat)
    lon = request.form.get('longitudechange')
    longitude = float(lon)
    items = {"deci_lat": [latitude], "deci_lon": [longitude]}
    df = pd.DataFrame(items)

    df = df[ (df['deci_lat']< 90.) & (df['deci_lat'] > -90.)]
    df = df[ (df['deci_lon']< 180.) & (df['deci_lon'] > -180.) ]

    if not df.empty:
        inRas=gdal.Open('stacked_bio_oracle_future/bio_oracle_future_stacked.tif')
        myarray=inRas.ReadAsArray()

        len_pd=np.arange(len(df))
        lon=df["deci_lon"]
        lat=df["deci_lat"]
        lon=lon.values
        lat=lat.values

        row=[]
        col=[]

        src=rasterio.open('stacked_bio_oracle_future/bio_oracle_future_stacked.tif', crs= 'espg: 4326')
        
        for i in len_pd:
            row_n, col_n = src.index(lon[i], lat[i])# spatial --> image coordinates
            row.append(row_n)
            col.append(col_n)
        
        mean_std=pd.read_csv('stacked_bio_oracle_future/future_env_bio_mean_std.txt',sep="\t")
        mean_std=mean_std.to_numpy()
        
        X=[]
        for j in range(0,9):
            print(j)
            band=myarray[j]
            x=[]
            
            for i in range(0,len(row)):
                value= band[row[i],col[i]]
                if value <-1000:
                    value=np.nan
                    x.append(value)
                else:
                    value = ((value - mean_std.item((j,1))) / mean_std.item((j,2))) # scale values
                    x.append(value)
            X.append(x)
        
        X.append(row)
        X.append(col)
        
        X =np.array([np.array(xi) for xi in X])
        
        df=pd.DataFrame(X)
        df=df.T
        df=df.dropna(axis=0, how='any')

        if not df.empty:
            input_X=df.loc[:,0:8]
            row=df[9]
            col=df[10]
            
            row_col=pd.DataFrame({"row":row,"col":col})
            
            input_X=input_X.values
            
            row=row.values
            col=col.values
            
            prediction_array=np.save('predictions/xgla_future_prediction_array.npy',input_X)
            prediction_pandas=row_col.to_csv('predictions/xgla__future_prediction_row_col.csv')
            
            input_X=np.load('predictions/xgla_future_prediction_array.npy')
            df=pd.DataFrame(input_X)
            
            new_band=myarray[1].copy()
            new_band.shape
            
            new_values = xip_gla_model_future.predict(x=input_X,verbose=0) ###predict output value
            new_band_values=[]
            
            for i in new_values:
                new_value=i[1]
                new_band_values.append(new_value)
                
            new_band_values=np.array(new_band_values)
            resultdf = pd.DataFrame(new_band_values, columns=['predicted_result'])
            val = resultdf['predicted_result'].values[0]   
            val = val*100
            vals = str(val)

            result = "Likeliood of presence: " + vals + "%"

            map = folium.Map(location=[latitude, longitude],zoom_start=8, tooltip = 'This tooltip will appear on hover')
            folium.Marker(location=[latitude,longitude], tooltip=result).add_to(map)
            map.save(outfile='templates/xglaf_map.html')

            return render_template('xglaf_map.html')

            #return map._repr_html_()


        else: 
            return render_template('land_coord.html')
    else:
        return render_template('invalid.html')

