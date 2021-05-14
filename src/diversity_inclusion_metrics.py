import numpy as np
from scipy.stats import gmean


class DIMetrics:
    """
    Diversity and Inclusion Metrics in Subset Selection (Mitchell et al., 2020)

    Diversity: Variety in the representation of individuals in an
    instance or set of instances, with respect to sociopoliti- cal
    power differentials (gender, race, etc.). Greater diversity
    means a closer match to a target distribution over socially
    relevant characteristics.

    Inclusion: Representation of an individual user within an instance
    or a set of instances, where greater inclusion corre- sponds to
    better alignment between a user and the options relevant to
    them in an instance or set.
    """

    def presence(self):
        """
        We define the presence score of an attribute `a`
        as a function quantifying how close the presence `a(xq )`
        is to the target and upper and lower bounds on
        the attribute’s presence:

        `Presence_(a)(x_(q))=f(a(x_(q)),l_(a),u_(a))`

        """
        pass

    def diversity(self):
        """
        Diversity Score. With the presence score defined, we can
        now define the diversity of an instance xq as an aggregate
        statistic of the attributes in the instance:

        `Diversity_(A)(x_(q))=g(" Presence "_(a)(x_(q)))`

        across a in A, where g(*) can return the minimum, maximum, or average presence value
        of the attributes.
        """
        pass

    def relevance(self):
        """
        Relevance of an item. Formally, let

        `rel(i,q)in[0,1]`

        measure the relevance of an item i to query q. The relevance
        score is an exoge- neous measure of how well an item answers
        a query, that is, it is the assumed system metric for the
        susbet selection task at hand.
        """
        pass

    def inclusion(self, Xi: list, p: dict, query: str) -> float:
        """
        X: collection of attributes
        p: person or individual
        q: query

        We can then define the inclusion of an instance as an aggregate
        statistic of the set of items in the instance, their relevance
        to the query, and the items’ alignment or match to individual p along a:

        `Inclusion_(a)(x_(q),p,q)=f(r_(x_(q)))in[-1,1]`

        An inclusion score near −1 indicates p finds the instance stereo- typical;
        this is similar to the notion of negative stereotypes in representation
        [10] or tokenism [33]. A score near 1 refers to p’s known attribute a
        being well aligned in xq . A score near 0 corresponds to p finding few
        or no attribute alignments in xq .
        """

        pass

    def representativeness(self, Xi: object, Pi: object) -> list:
        """
        Inclusion here is equal to the representativeness 
        score for each group type
        
        `rep_(a)(i,p,q)`
        """
        
        rep_scores: list = []
        for group_type in list(Xi.__annotations__.keys()):
            rep: callable = Xi.__getattribute__(f"representativeness_{group_type}")
            rep_scores.append(
                rep(
                    Xi.__getattribute__(group_type), Pi.__getattribute__(group_type)
                )  # , query?
            )

        return rep_scores

    @staticmethod
    def utilitarian_inclusivity(scores: list) -> list:
        """
        Utilitarian inclusivity: This corresponds to an arithmetic
        average over the inclusion scores for all items in the set,
        where a set X_1 is more inclusive than X_2 if the average of
        its inclusion metric scores is greater.

        `(1)/(n)sum_(i)X_(2i)<(1)/(n)sum_(i)X_(1i)`
        """
        return [np.mean(x) for x in scores]

    @staticmethod
    def nash_inclusivity(scores: list) -> list:
        """
        Nash inclusivity: This corresponds to the geometric mean over
        the inclusion scores for all items in the set. Set X1 is more
        inclusive than X2 if the product of its inclusion metric
        scores is greater

        `root(n)(prod_(i)X_(2i))<root(n)(prod_(i)X_(1i))`
        """

        return [gmean(x) for x in scores]

    @staticmethod
    def egalitarian_inclusivity(scores: list) -> list:
        """
        Egalitarian (maximin) inclusivity. Set X_1 may be said to be more
        inclusive than set X_2 if the lowest inclusion score in X_1 is higher
        than the lowest inclusion score in X_2, i.e.,

        `min_(i)(X_(1i))>min_(i)(X_(2i))`

        If `min_(i)(X_(1i)) = min_(i)(X_(2i)), then repeat for the second lowest scores,
        third, and so on. If the two mechanisms are equal, we are
        indifferent between X_1 and X_2.
        """

        return [min(x) for x in scores]

    def prompt_polarity(self):
        """
        Prompt Polarity. When applying Diversity and Inclusion metrics in a domain
        where the query is not only neutral, but may also be negative (e.g., “jerks”),
        it is necessary to incorporate a polarity(q) value into the score to tease
        out the ‘negative’ meaning and values of the inclusion score, as may be
        provided by a sentiment model. For example:

        `rep_(a)(i,p,q)=I[a({i})=a({p})]**lambda" polarity "(q)`
        """
        pass
