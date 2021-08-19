import matplotlib.pyplot as plt
import numpy as np

class queue:
    def __init__(self, Amazon, Netflix, Scenario):
        self.Amazon_average_arrival_rate = Amazon[0]
        self.Amazon_average_service_rate = Amazon[1]
        self.Netflix_average_arrival_rate = Netflix[0]
        self.Netflix_average_service_rate = Netflix[1]
        self.Scenario = Scenario
        self.run_time = 1000000

    def queue_length(self):
        self.Amazon_q = np.zeros(self.run_time, dtype=int)
        self.Netflix_q = np.zeros(self.run_time, dtype=int)

        for i in range(len(self.Amazon_q)):
            a1 = np.random.binomial(1, self.Amazon_average_arrival_rate)
            s1 = np.random.binomial(1, self.Amazon_average_service_rate)
            if i < len(self.Amazon_q) - 1:
                self.Amazon_q[i+1] = max(self.Amazon_q[i] + a1 - s1, 0)

        for i in range(len(self.Netflix_q)):
            a1 = np.random.binomial(1, self.Netflix_average_arrival_rate)
            s1 = np.random.binomial(1, self.Netflix_average_service_rate)
            if i < len(self.Netflix_q) - 1:
                self.Netflix_q[i+1] = max(self.Netflix_q[i] + a1 - s1, 0)


    def state_distribution(self):
        self.queue_length()
        self.max_amazon_queue = np.amax(self.Amazon_q)
        self.max_netflix_queue = np.amax(self.Netflix_q)
        self.Amazon_empirical_occupancy = np.zeros(self.max_amazon_queue + 1)
        self.Netflix_empirical_occupancy = np.zeros(self.max_netflix_queue + 1)

        for i in range(len(self.Amazon_q)):
            self.Amazon_empirical_occupancy[self.Amazon_q[i]] = self.Amazon_empirical_occupancy[self.Amazon_q[i]] + 1
        self.Amazon_empirical_occupancy = self.Amazon_empirical_occupancy / self.run_time

        for i in range(len(self.Netflix_q)):
            self.Netflix_empirical_occupancy[self.Netflix_q[i]] = self.Netflix_empirical_occupancy[self.Netflix_q[i]] + 1
        self.Netflix_empirical_occupancy = self.Netflix_empirical_occupancy / self.run_time

        self.Amazon_theoretical_occupancy = np.zeros(self.max_amazon_queue + 1)
        self.Netflix_theoretical_occupancy = np.zeros(self.max_netflix_queue + 1)

        self.rho = (self.Amazon_average_arrival_rate * (1 - self.Amazon_average_service_rate)) / \
                   (self.Amazon_average_service_rate * (1 - self.Amazon_average_arrival_rate))
        for i in range(len(self.Amazon_theoretical_occupancy)):
            self.Amazon_theoretical_occupancy[i] = (self.rho ** i) * (1 - self.rho)

        self.rho1 = (self.Netflix_average_arrival_rate * (1 - self.Netflix_average_service_rate)) / \
                    (self.Netflix_average_service_rate * (1 - self.Netflix_average_arrival_rate))
        for i in range(len(self.Netflix_theoretical_occupancy)):
            self.Netflix_theoretical_occupancy[i] = (self.rho1 ** i) * (1 - self.rho1)
        return

    def display_state_distribution(self):
        self.state_distribution()
        t = np.arange(0, self.max_amazon_queue + 1, dtype=int)
        plt.scatter(t, self.Amazon_empirical_occupancy)
        plt.scatter(t, self.Amazon_theoretical_occupancy)
        plt.xlabel("Queue size")
        plt.ylabel("Probability")
        plt.title("amazon_state_distribution - "+self.Scenario)
        plt.show()

        t1 = np.arange(0, self.max_netflix_queue + 1, dtype=int)
        plt.scatter(t1, self.Netflix_empirical_occupancy)
        plt.scatter(t1, self.Netflix_theoretical_occupancy)
        plt.xlabel("Queue size")
        plt.ylabel("Probability")
        plt.title("netflix_state_distribution - "+self.Scenario)
        plt.show()

    def avg_q_length(self):
        self.amazon_emp_avg_q_len = np.zeros(len(self.Amazon_q))
        self.netflix_emp_avg_q_len = np.zeros(len(self.Netflix_q))
        for k in range(len(self.Amazon_q)):
            if k == 0:
                self.amazon_emp_avg_q_len[0] = self.Amazon_q[0]
            else:
                self.amazon_emp_avg_q_len[k] = (((k - 1) * self.amazon_emp_avg_q_len[k - 1]) + self.Amazon_q[k]) / k
            k += 1

        for k in range(len(self.Netflix_q)):
            if k == 0:
                self.netflix_emp_avg_q_len[0] = self.Netflix_q[0]
            else:
                self.netflix_emp_avg_q_len[k] = (((k - 1) * self.netflix_emp_avg_q_len[k - 1]) + self.Netflix_q[k]) / k
            k += 1

        self.amazon_theo_avg_q_len = np.zeros(len(self.Amazon_q))
        self.netflix_theo_avg_q_len = np.zeros(len(self.Netflix_q))
        for k in range(len(self.Amazon_q)):
            self.amazon_theo_avg_q_len[k] = self.rho / (1 - self.rho)
        for k in range(len(self.Netflix_q)):
            self.netflix_theo_avg_q_len[k] = self.rho1 / (1 - self.rho1)
        return

    def display_avg_q_length(self):
        self.avg_q_length()
        t = np.arange(0, len(self.Amazon_q), dtype=int)
        plt.scatter(t, self.amazon_emp_avg_q_len)
        plt.scatter(t, self.amazon_theo_avg_q_len)
        plt.xlabel("Timeslots")
        plt.ylabel("Average Queue Length")
        plt.ylabel("Average Queue Length")
        plt.title("amazon_average_queue_length - "+self.Scenario)
        plt.show()

        t1 = np.arange(0, len(self.Netflix_q), dtype=int)
        plt.scatter(t1, self.netflix_emp_avg_q_len)
        plt.scatter(t1, self.netflix_theo_avg_q_len)
        plt.xlabel("Timeslots")
        plt.ylabel("Average Queue Length")
        plt.title("netflix_average_queue_length - " +self.Scenario)
        plt.show()

    def isp_revenue(self):
        self.queue_length()
        self.p = []
        self.p = np.arange(0, 1.1, .1)  # probability of multiplexer
        self.isp_total_revenue = np.zeros(self.run_time, dtype=float)  # array
        self.isp_total_revenue_total_p = np.zeros(11, dtype=float)
        self.expected_revenue = np.zeros(11, dtype=float)  # theoretical revenue
        for k in range(len(self.p)):
            for m in range(self.run_time):
                is_l1_activated = np.random.binomial(1, self.p[k])
                if is_l1_activated == 1:
                    is_l2_activated = 0
                else:
                    is_l2_activated = 1
                if self.Amazon_q[m] != 0:
                    amazon_serviced = np.random.binomial(1, self.Amazon_average_service_rate)
                else:
                    amazon_serviced = 0
                if self.Netflix_q[m] != 0:
                    netflix_serviced = np.random.binomial(1, self.Netflix_average_service_rate)
                else:
                    netflix_serviced = 0
                if m == 0:
                    self.isp_total_revenue[m] = 0
                else:
                    self.isp_total_revenue[m] = self.isp_total_revenue[m - 1] + (is_l2_activated * amazon_serviced * 50) + \
                                                (is_l1_activated * netflix_serviced * 40)
            self.isp_total_revenue_total_p[k] = self.isp_total_revenue[999999] / self.run_time
            self.expected_revenue[k] = (self.Amazon_average_service_rate * self.rho * (1 - self.p[k]) * 50) + \
                                       (self.Netflix_average_service_rate * self.rho1 * self.p[k] * 40)
        return

    def display_isp_revenue(self):
        self.isp_revenue()
        plt.scatter(self.p, self.isp_total_revenue_total_p)
        plt.scatter(self.p, self.expected_revenue)
        plt.xlabel("probability")
        plt.ylabel("isp_revenue")
        plt.title("Emperical_vs_Theoretical_ISP_revenue - " + self.Scenario)
        plt.show()

    def ISP_state_distribution(self,isp_average_service_rate):
        self.state_distribution()
        self.isp_q = np.zeros(self.run_time, dtype=int)
        p=0  #optimal value
        self.isp_average_arrival_rate= (self.Amazon_average_service_rate*self.rho*(1-p)) + \
                                       (self.Netflix_average_service_rate*self.rho1*p)

        for i in range(len(self.isp_q)):
            a1 = np.random.binomial(1, self.isp_average_arrival_rate)
            s1 = np.random.binomial(1, isp_average_service_rate)
            if i < len(self.isp_q) - 1:
                self.isp_q[i+1] = max(self.isp_q[i] + a1 - s1, 0)
        #Emperical value
        self.max_isp_queue = np.amax(self.isp_q)
        self.isp_empirical_occupancy = np.zeros(self.max_isp_queue + 1)
        for i in range(len(self.isp_q)):
            self.isp_empirical_occupancy[self.isp_q[i]] = self.isp_empirical_occupancy[self.isp_q[i]] + 1
        self.isp_empirical_occupancy = self.isp_empirical_occupancy / self.run_time

        #theoretical value
        self.isp_theoretical_occupancy = np.zeros(self.max_isp_queue + 1)
        self.rho3 = (self.isp_average_arrival_rate * (1 - isp_average_service_rate)) / \
                    (isp_average_service_rate * (1 - self.isp_average_arrival_rate))
        for i in range(len(self.isp_theoretical_occupancy)):
            self.isp_theoretical_occupancy[i] = (self.rho3 ** i) * (1 - self.rho3)

        return

    def display_ISP_state_distribution(self,isp_average_service_rate):
        self.ISP_state_distribution(isp_average_service_rate)
        t = np.arange(0, self.max_isp_queue + 1, dtype=int)
        plt.scatter(t, self.isp_empirical_occupancy)
        plt.scatter(t, self.isp_theoretical_occupancy)
        plt.xlabel("Queue size")
        plt.ylabel("Probability")
        plt.title("isp_state_distribution - "+self.Scenario)
        plt.show()

    def isp_avg_q_length(self,isp_average_service_rate):
        self.ISP_state_distribution(isp_average_service_rate)
        #emperical value
        self.isp_emp_avg_q_len = np.zeros(len(self.isp_q))
        for k in range(len(self.isp_q)):
            if k == 0:
                self.isp_emp_avg_q_len[0] = self.isp_q[0]
            else:
                self.isp_emp_avg_q_len[k] = (((k - 1) * self.isp_emp_avg_q_len[k - 1]) + self.isp_q[k]) / k
            k += 1
        #theoretical value
        self.isp_theo_avg_q_len = np.zeros(len(self.isp_q))
        for k in range(len(self.isp_q)):
            self.isp_theo_avg_q_len[k] = self.rho3 / (1 - self.rho3)
        return

    def display_isp_avg_q_length(self,isp_average_service_rate):
        self.isp_avg_q_length(isp_average_service_rate)
        t1 = np.arange(0, len(self.isp_q), dtype=int)
        plt.scatter(t1, self.isp_emp_avg_q_len)
        plt.scatter(t1, self.isp_theo_avg_q_len)
        plt.xlabel("Timeslots")
        plt.ylabel("Average Queue Length")
        plt.title("isp_average_queue_length - " + self.Scenario)
        plt.show()

#Scenario1
Amazon_scenario1=[0.4,0.5]
Netflix_scenario1=[0.5,0.6]
Q1=queue(Amazon_scenario1,Netflix_scenario1,"Scenario1")
Q1.display_state_distribution()
Q1.display_avg_q_length()
Q1.display_isp_revenue()
Q1.display_ISP_state_distribution(0.8)
Q1.display_isp_avg_q_length(0.8)

#Scenario2
Amazon_scenario2=[0.45,0.5]
Netflix_scenario2=[0.55,0.6]
Q2=queue(Amazon_scenario2,Netflix_scenario2,"Scenario2")
Q2.display_state_distribution()
Q2.display_avg_q_length()
Q2.display_isp_revenue()
Q2.display_ISP_state_distribution(0.8)
Q2.display_isp_avg_q_length(0.8)

#Scenario3
Amazon_scenario3=[0.49,0.5]
Netflix_scenario3=[0.59,0.6]
Q3=queue(Amazon_scenario3,Netflix_scenario3,"Scenario3")
Q3.display_state_distribution()
Q3.display_avg_q_length()
Q3.display_isp_revenue()
Q3.display_ISP_state_distribution(0.8)
Q3.display_isp_avg_q_length(0.8)




