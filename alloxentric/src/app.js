import axios from 'axios';

export default {
  data() {
    return {
      plans: [],
    };
  },
  methods: {
    async fetchPlans() {
      try {
        const response = await axios.get('http://localhost:8000/plans');
        this.plans = response.data;
      } catch (error) {
        console.error("Error fetching plans:", error);
      }
    },
  },
  mounted() {
    this.fetchPlans();
  },
};

