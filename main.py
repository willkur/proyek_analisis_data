class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    def create_daily_orders_df(self):
        daily_orders_df = (self.df.resample(rule='D', on='order_approved_at')
                           .agg(order_count=('order_id', 'nunique'),
                                revenue=('payment_value', 'sum')))
        return daily_orders_df.reset_index()

    def create_sum_spend_df(self):
        sum_spend_df = (self.df.resample(rule='D', on='order_approved_at')
                        .agg(total_spend=('payment_value', 'sum')))
        return sum_spend_df.reset_index()

    def create_sum_order_items_df(self):
        sum_order_items_df = (self.df.groupby("product_category_name_english")
                              .agg(product_count=('product_id', 'count'))
                              .reset_index()
                              .sort_values(by='product_count', ascending=False))
        return sum_order_items_df

    def review_score_df(self):
        review_scores = self.df['review_score'].value_counts().sort_values(ascending=False)
        most_common_score = review_scores.idxmax()
        return review_scores, most_common_score

    def create_bystate_df(self):
        bystate_df = (self.df.groupby("customer_state")
                      .agg(customer_count=('customer_id', 'nunique'))
                      .reset_index()
                      .sort_values(by='customer_count', ascending=False))
        most_common_state = bystate_df.loc[bystate_df['customer_count'].idxmax(), 'customer_state']
        return bystate_df, most_common_state
    
    def create_bygender_df(self):
        bygender_df = (self.df.groupby("gender")
                       .agg(customer_count=('customer_id', 'nunique'))
                       .reset_index())
        return bygender_df

    def create_order_status(self):
        order_status_df = self.df["order_status"].value_counts().sort_values(ascending=False)
        most_common_status = order_status_df.idxmax()
        return order_status_df, most_common_status
    
class BrazilMapPlotter:
    def __init__(self, data, plt, mpimg, urllib, st):
        self.data = data
        self.plt = plt
        self.mpimg = mpimg
        self.urllib = urllib
        self.st = st

    def plot(self):
        brazil_image_url = 'https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'
        brazil = self.mpimg.imread(self.urllib.request.urlopen(brazil_image_url), 'jpg')

        fig, ax = self.plt.subplots(figsize=(10, 10))

        self.data.plot(
            kind="scatter", 
            x="geolocation_lng", 
            y="geolocation_lat",
            alpha=0.3, 
            s=0.3, 
            color='maroon',
            ax=ax
        )

        ax.axis('off')
        ax.imshow(brazil, extent=[-73.98283055, -33.8, -33.75116944, 5.4])

        self.st.pyplot(fig)

        self.plt.close(fig)