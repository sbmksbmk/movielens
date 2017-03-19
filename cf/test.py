import sys
from recommendation import sbmk_train


def main(train="", test=""):
    st = sbmk_train()
    st.load(path=train)
    st.testing(path=test)
    # data = st.get_training_data()

    """
    m_sim = 0
    m_rel = 0
    per1 = None
    per2 = None
    keys = data.keys()
    for i in range(len(keys) - 1):
        for j in range(i + 1, len(keys)):
            sim = st.get_sim(data[keys[i]].copy(), data[keys[j]].copy())
            rel = st.get_correlation(data[keys[i]].copy(), data[keys[j]].copy())
            if sim > m_sim or rel > m_rel:
                m_sim = sim
                m_rel = rel
                per1 = keys[i]
                per2 = keys[j]
                if sim >= 0.7 or rel >= 0.7:
                    print per1, per2, sim, rel, len(set(data[per1].keys()).intersection(set(data[per2].keys())))
    print per1, per2
    return m_sim, m_rel, data[per1], data[per2]
    """
    return None

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "python test.py TRAIN_PATH TEST_PATH"
        exit()
    main(train=sys.argv[1], test=sys.argv[2])
    """
    sim, rel, p1, p2 = main(train=sys.argv[1], test=sys.argv[2])
    print sim, rel
    print p1
    print "======================================"
    print p2
    print "======================================"
    print set(p1.keys()).intersection(set(p2.keys()))
    """