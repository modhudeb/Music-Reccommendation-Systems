import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from HelpHand import GetHand
import sys


class MetaFilter(BaseEstimator, TransformerMixin, GetHand):
    """
    Before Using this algorithm, Make sure you have following columns in your `Tracks Dataframe` :\n
    ['name', 'popularity', 'artists', 'danceability', 'energy', 'acousticness', 'instrumentalness', 'valence', 'year']\n
    `These column's name should be as it is shown`
    """
    def __init__(self):
        self.df = pd.DataFrame()
        self.adf = pd.DataFrame()
        self.final_df = pd.DataFrame()
        self.artists = []
        self._recommendedSong= pd.DataFrame()
        self.exit = 0
        return None



    def fit(self, X: list, y=None):
        """
        Pass 2 DataFrame in a `list`. First one is `Tracks dataframe` and second one is `Artists dataframe`

        Example:
        --------
        >>> mf = MetaFilter()
        >>> mf.fit(X = [tdf, adf])
        """
        self.df = X[0]
        self.adf = X[1]
        self.final_df = pd.DataFrame(columns=self.df.columns)
        return "Fitted"
        
        



    def transform(self, X: list):
        X = self.final_df
        return X



    def fit_transform(self, X, y=None):
        return self.transform(X)


    def getRecommendation(self, df:pd.DataFrame):
        """
        Pass your `artists dataset`
        """
        artists_df = df
        recommend_songs_df = self.final_df
        recommend_songs_array = []
        recommend_songs_popu = []
        recommend_songs_artist = []
        recommend_songs_artist_popu = []
        inp_art_popu = []

        for x in self.artists:
            popu = GetHand.firstValueOf(artists_df[artists_df['name'] == x], 'popularity')
            inp_art_popu.append(popu)
            


        for x in range(len(recommend_songs_df)):
            song_name = recommend_songs_df['name'].loc[recommend_songs_df.index[x]]
            song_popu = recommend_songs_df['popularity'].loc[recommend_songs_df.index[x]]
            singer = recommend_songs_df['artists'].loc[recommend_songs_df.index[x]]

            if len(artists_df[artists_df['name'] == singer]) == 0:
                continue
            else:
                singersPopularity = GetHand.firstValueOf(artists_df[artists_df['name'] == singer], 'popularity')
                for popu in inp_art_popu:
                    if (popu-5) <= singersPopularity <= (popu+20):
                        # song = f"{name} by {singer}"                        
                        recommend_songs_array.append(song_name)
                        recommend_songs_popu.append(song_popu)
                        recommend_songs_artist.append(singer)
                        recommend_songs_artist_popu.append(singersPopularity)
                        break

        recDf = pd.DataFrame(columns=['song', 'songPopu', 'artists', 'artistPopu'])
        recDf['song'] = np.array(recommend_songs_array)
        recDf['songPopu'] = np.array(recommend_songs_popu)
        recDf['artists'] = np.array(recommend_songs_artist)
        recDf['artistPopu'] = np.array(recommend_songs_artist_popu)
        return recDf




    def predict(self, X:list):
        """
        Pass 2 or more songs in a list.

        Example:
        --------
        >>> mf = MetaFilter()
        >>> mf.fit(X = [tdf, adf])
        >>> mf.predict(X = ['Havana by camila', 'shape of you', 'into you by ari'])
        """
        
        X = list(map(lambda x: x.lower(), X))
        yr = 0
        ppt = 0
        vc = 0
        iml = 0
        eg = 0
        ac = 0
        da = 0
        xdf = pd.DataFrame(columns=self.df.columns) # we will concat input song's data with this xdf (in further)
        
        self.exit = 0
        # Getting rank
        for i in range(len(X)):
            sdf = GetHand.isExist(self.df, string=X[i])
            if sdf is None:
                continue
            else:
                self.exit += 1
                sdf = sdf.sort_values(by=['popularity', 'year'], ascending=False)
                year = GetHand.firstValueOf(sdf, 'year')
                popularity = GetHand.firstValueOf(sdf, 'popularity')
                valence = GetHand.firstValueOf(sdf, 'valence')
                instrumentalness = GetHand.firstValueOf(sdf, 'instrumentalness')
                acousticness = GetHand.firstValueOf(sdf, 'acousticness')
                energy = GetHand.firstValueOf(sdf, 'energy')
                danceability = GetHand.firstValueOf(sdf, 'danceability')
                artists = GetHand.firstValueOf(sdf, 'artists')
                self.artists.append(artists)
                if 2018 <= year <= 2022:
                    yr += 1
                if 80 <= popularity <= 100:
                    ppt += 1
                if 0.7 <= valence <= 1.00:
                    vc += 1
                if 0.76 <= instrumentalness <= 1.00:
                    iml += 1
                if 0.8 <= acousticness <= 1.00:
                    ac += 1
                if 0.7 <= energy <= 1.00:
                    eg += 1
                if 0.68 <= danceability <= 1.00:
                    da += 1
                ###################################
                xdf = pd.concat([xdf, sdf[0:1]])
        # for loop end
        if self.exit == 0:
            return sys.exit("No song found. Please check the song name or artist name")

        chart = {"year":yr,"popularity": ppt, "valence": vc, "instrumentalness": iml,
                 "acousticness": ac, "energy": eg, "danceability": da}
        store = chart.copy()
        rank = []
        for x in range(len(store)):
            mx = max(store, key=store.get)
            rank.append(mx)
            store.pop(mx)

        # xdf is user input song's DataFrame
        # getting recommendations
        topRank=[]
        for x in range(len(xdf)):
            for rk in rank:
                if rk == "year":
                    val = xdf['year'].loc[xdf.index[x]]
                    yr = self.df['year'].between((val-1), (2+val))
                    topRank.append(yr)

                if rk == "popularity":
                    val = xdf['popularity'].loc[xdf.index[x]]
                    ppt = self.df['popularity'].between((val-5), (5+val))
                    topRank.append(ppt)

                if rk == "valence":
                    val = xdf['valence'].loc[xdf.index[x]]
                    vc = self.df['valence'].between((val/100*95), (val/100*120))
                    topRank.append(vc)

                if rk == "instrumentalness":
                    val = xdf['instrumentalness'].loc[xdf.index[x]]
                    iml = self.df['instrumentalness'].between((val/100*95), (val/100*110))
                    topRank.append(iml)

                if rk == "acousticness":
                    val = xdf['acousticness'].loc[xdf.index[x]]
                    ac = self.df['acousticness'].between((val/100*95), (val/100*110))
                    topRank.append(ac)

                if rk == "energy":
                    val = xdf['energy'].loc[xdf.index[x]]
                    eg = self.df['energy'].between((val/100*95), (val/100*115))
                    topRank.append(eg)

                if rk == "danceability":
                    val = xdf['danceability'].loc[xdf.index[x]]
                    da = self.df['danceability'].between((val/100*95), (val/100*115))
                    topRank.append(da)
            #########################################################################################

            temp = self.df[topRank[0] & topRank[1] | (topRank[2] & topRank[3])].sort_values(by=rank, ascending=False)
            self.final_df = pd.concat([self.final_df, temp]).drop_duplicates(keep='first')

            #########################################################################################

        self._recommendedSong = self.getRecommendation(self.adf)
        print(rank)
        ###########################
        recommend_songs_df = self._recommendedSong
        recommend_songs_df = recommend_songs_df.sort_values(by=['songPopu','artistPopu'], ascending=False, ignore_index=True)
        self.recommend_songs_df = recommend_songs_df.head(50) 

        rec_song_array = []
        for x in range(len(self.recommend_songs_df)) :
            song = self.recommend_songs_df['song'].loc[self.recommend_songs_df.index[x]]
            singer = self.recommend_songs_df['artists'].loc[self.recommend_songs_df.index[x]]
            rec_song_array.append(f"{song} by {singer}")

        return rec_song_array



