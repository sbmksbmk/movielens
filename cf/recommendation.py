from math import sqrt
from scipy import spatial


class sbmk_train(object):
    def __init__(self):
        pass

    def get_training_data(self):
        return self.training_data

    def load(self, path=None, skipline=1, splitter='\t'):
        if path is None:
            print "Path is None!!"
            return
        self.training_data = {}
        with open(path, 'r') as fn:
            lns = fn.readlines()[skipline:]
            for ln in lns:
                sp = ln.split(splitter)
                # data format should be => userID, movieID, ranking, timestamp
                try:
                    self.training_data[sp[0]][sp[1]] = float(sp[2])
                except:
                    # new user ID in training_data
                    # import pdb; pdb.set_trace()
                    self.training_data[sp[0]] = {sp[1]: float(sp[2])}

    def testing(self, path=None, skipline=0, splitter='\t'):
        if path is None:
            print "Testing data path is None!!"
            return
        test_data = {}
        with open(path, 'r') as fn:
            lns = fn.readlines()[skipline:]
            for ln in lns:
                sp = ln.split(splitter)
                # data format should be => userID, movieID, ranking, timestamp
                try:
                    test_data[sp[0]][sp[1]] = float(sp[2])
                except:
                    # new user ID in training_data
                    test_data[sp[0]] = {sp[1]: float(sp[2])}

        hit_ranking_range = 0
        hit_result = {}
        # {uid: {moiveid: [test_ranking, rec_ranking]}}
        total_test_data = 0
        accept_diff = 0.2
        for i in range(0, 10):
            hit_ranking_range = 0
            hit_result = {}
            # {uid: {moiveid: [test_ranking, rec_ranking]}}
            total_test_data = 0
            for uid in test_data.keys():
                # result = self.rec_for_user(self.training_data.get(uid, {}).copy())
                result = self.rec_eng(uid, self.training_data.get(uid, {}).copy(), i / 10.0)
                for mid, ranking in test_data[uid].items():
                    total_test_data += 1
                    rr = float(result.get(mid, 10))
                    if abs(ranking - rr) / ranking <= accept_diff:
                        hit_ranking_range += 1
                        try:
                            hit_result[uid][mid] = [ranking, rr]
                        except:
                            hit_result[uid] = {mid: [ranking, rr]}
            # print hit_result
            print "in {},  {} %".format(i / 10.0, float(hit_ranking_range) / total_test_data)

    def rec_for_user(self, userdata={}):
        # find others like userdata from self.training_data data
        least_same = len(userdata) * 0.5
        like_users = {}
        user_set = set(userdata.keys())
        reckey = set()
        for userid, sub_user in self.training_data.items():
            # import pdb; pdb.set_trace()
            same_keys = set(sub_user.keys()).intersection(user_set)
            sub_user['same_keys'] = len(same_keys)
            s = 0
            for key in same_keys:
                try:
                    diff = (userdata[key] - sub_user[key]) / userdata[key]
                    s += (diff * diff)
                except Exception as e:
                    print userdata
                    print str(e)
                    exit()
            sub_user['all_diff'] = s
            try:
                sub_user['avg_diff'] = ((float(s)) ** 0.5) / sub_user['same_keys']
            except:
                sub_user['avg_diff'] = 5.0
            if len(same_keys) >= least_same and sub_user['avg_diff'] <= 1.0:
                for key in same_keys:
                    sub_user.pop(key, None)

                like_users.update({userid: sub_user})
                reckey = reckey.union(set(sub_user.keys()))
            reckey.add('all_diff')
            reckey.add('avg_diff')
            reckey.add('same_keys')
        # sort = sorted(like_users.values(), key=itemgetter('avg_diff'))
        # print sort
        rec = {}
        rec_limit = len(like_users) / 2
        reckey.remove('all_diff')
        reckey.remove('avg_diff')
        reckey.remove('same_keys')
        for key in reckey:
            count = 0
            s = 0
            for uv in like_users.values():
                try:
                    s += uv[key]
                    count += 1
                except:
                    pass
            if count >= rec_limit:
                rec[key] = float(s) / count

        return rec

    def rec_eng(self, uid="", userdata={}, limit=0.8):
        umovie_id_set = set(userdata.keys())
        all_id = set(self.training_data.keys())
        try:
            all_id.remove(uid)
        except:
            pass
        movie_ranking = {}
        # movie ranking = sum(sim * rank) / sum(sim)
        for oid in all_id:
            oid_set = set(self.training_data[oid])
            sim = self.get_correlation(self.training_data[oid], userdata, oid_set, umovie_id_set)
            if sim >= limit:
                diff_moive_id = oid_set.difference(umovie_id_set)
                for movie_id in diff_moive_id:
                    try:
                        movie_ranking[movie_id]['total'] += sim * self.training_data[oid][movie_id]
                        movie_ranking[movie_id]['simsum'] += sim
                    except:
                        movie_ranking[movie_id] = {'total': sim * self.training_data[oid][movie_id],
                                                   'simsum': sim}
        rec = {}
        for movie_id, result in movie_ranking.items():
            rec[movie_id] = result['total'] / result['simsum']
        return rec

    def get_sim(self, person_one={}, person_two={}):
        both_viewed = set(person_one.keys()).intersection(set(person_two.keys()))

        # Conditions to check they both have an common rating items
        if len(both_viewed) == 0:
            return 0

        # Finding Euclidean distance
        sum_of_eclidean_distance = 0

        for item in both_viewed:
            sum_of_eclidean_distance += pow(person_one[item] - person_two[item], 2)

        return 1 / (1 + sqrt(sum_of_eclidean_distance))

    def get_correlation(self, person_one={}, person_two={}, person_one_set=set(), person_two_set=set()):
        both_rated = set(person_one.keys()).intersection(set(person_two.keys()))
        number_of_ratings = len(both_rated)
        # Conditions to check they both have an common rating items
        if number_of_ratings == 0:
            return -1

        # Add up all the preferences of each user
        person1_preferences_sum = sum([person_one[item] for item in both_rated])
        person2_preferences_sum = sum([person_two[item] for item in both_rated])

        # Sum up the squares of preferences of each user
        person1_square_preferences_sum = sum([pow(person_one[item], 2) for item in both_rated])
        person2_square_preferences_sum = sum([pow(person_two[item], 2) for item in both_rated])

        # Sum up the product value of both preferences for each item
        product_sum_of_both_users = sum([person_one[item] * person_two[item] for item in both_rated])

        # Calculate the pearson score
        numerator_value = product_sum_of_both_users - (person1_preferences_sum * person2_preferences_sum / number_of_ratings)
        denominator_value = sqrt((person1_square_preferences_sum - pow(person1_preferences_sum, 2) / number_of_ratings) * (person2_square_preferences_sum - pow(person2_preferences_sum, 2) / number_of_ratings))
        if denominator_value == 0 or numerator_value == 0:
            return -1
        else:
            r = numerator_value / denominator_value
            return r


class movie_train(object):
    def __init__(self):
        self.trainer_key = {}

    def get_training_data(self):
        return self.training_data

    def load(self, training_data):
        """
        training_data format as follow
        {
            trainer_id:{
                {movie_id: raing},
                {movie_id: raing},
            },
            trainer_id:{
                {movie_id: raing},
                {movie_id: raing},
            },
        }
        """
        self.training_data = training_data

    def add_trainer_info(self, trainer_info):
        for user_id, user_info in trainer_info.items():
            for key, value in user_info.items():
                self.training_data[user_id][key] = value

    def get_recommendation(self, userdata={}, limit=0.3, return_max=100):
        umovie_id_set = set(userdata.keys())
        for key in self.trainer_key:
            # add trainer_key into umovie_id_set make sure these keys will not into movie_ranking
            umovie_id_set.add(key)
        all_id = set(self.training_data.keys())
        movie_ranking = {}
        # movie ranking = sum(sim * rank) / sum(sim)
        # Calculate all relation from training data with userdata

        if len(userdata) < 10:
            # why 10... no reason...
            compaire_method = self.get_cos_sim
        else:
            compaire_method = self.get_correlation

        for oid in all_id:
            oid_set = set(self.training_data[oid])
            sim = compaire_method(self.training_data[oid], userdata)
            # print sim
            if sim >= limit:
                diff_moive_id = oid_set.difference(umovie_id_set)
                for movie_id in diff_moive_id:
                    try:
                        movie_ranking[movie_id]['total'] += sim * self.training_data[oid][movie_id]
                        movie_ranking[movie_id]['simsum'] += sim
                    except:
                        movie_ranking[movie_id] = {'total': sim * self.training_data[oid][movie_id],
                                                   'simsum': sim}
            else:
                # print oid, sim
                pass
        rec = {}
        # print movie_ranking
        for movie_id, result in movie_ranking.items():
            try:
                rec[movie_id] = result['total'] / result['simsum']
            except:
                rec[movie_id] = 0
        return_len = min(return_max, len(rec))
        return sorted(rec.items(), key=lambda x: x[1], reverse=True)[:return_len]

    def get_sim(self, training_user={}, userdata={}):
        both_viewed = set(training_user.keys()).intersection(set(userdata.keys()))

        # Conditions to check they both have an common rating items
        if len(both_viewed) == 0:
            return 0

        # Finding Euclidean distance
        sum_of_eclidean_distance = 0

        for item in both_viewed:
            # print training_user[item], userdata[item]
            sum_of_eclidean_distance += pow(training_user[item] - userdata[item], 2)
        return 1 / (1 + sqrt(sum_of_eclidean_distance))

    def get_correlation(self, training_user={}, userdata={}):
        both_rated = set(training_user.keys()).intersection(set(userdata.keys()))
        number_of_ratings = len(both_rated)
        # Conditions to check they both have an common rating items
        if number_of_ratings == 0:
            return -1

        # Add up all the preferences of each user
        person1_preferences_sum = sum([training_user[item] for item in both_rated])
        person2_preferences_sum = sum([userdata[item] for item in both_rated])

        # Sum up the squares of preferences of each user
        person1_square_preferences_sum = sum([pow(training_user[item], 2) for item in both_rated])
        person2_square_preferences_sum = sum([pow(userdata[item], 2) for item in both_rated])

        # Sum up the product value of both preferences for each item
        product_sum_of_both_users = sum([training_user[item] * userdata[item] for item in both_rated])

        # Calculate the pearson score
        numerator_value = product_sum_of_both_users - (person1_preferences_sum * person2_preferences_sum / number_of_ratings)
        denominator_value = sqrt((person1_square_preferences_sum - pow(person1_preferences_sum, 2) / number_of_ratings) * (person2_square_preferences_sum - pow(person2_preferences_sum, 2) / number_of_ratings))
        if denominator_value == 0:
            return -1
        else:
            r = numerator_value / denominator_value
            return r

    def get_cos_sim(self, training_user={}, userdata={}):
        both_rated = set(training_user.keys()).intersection(set(userdata.keys()))
        # print both_rated
        number_of_ratings = len(both_rated)
        # Conditions to check they both have an common rating items
        if number_of_ratings == 0:
            return -1
        if number_of_ratings == 1:
            # prevent only one rating data will return 1
            item = both_rated.pop()
            return (5 - abs(training_user[item] - userdata[item])) / 5
        cos_arr_train = []
        cos_arr_user = []
        for item in both_rated:
            cos_arr_train.append(training_user[item])
            cos_arr_user.append(userdata[item])
        return 1 - spatial.distance.cosine(cos_arr_train, cos_arr_user)
