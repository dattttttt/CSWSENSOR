<template>
  <div>
    <h1>CSW Sensor Monitor</h1>

    <div>
      <h2>Nút bấm</h2>
      <p>{{ button.tohop }} ({{ button.time }})</p>
    </div>

    <div>
      <h2>Trạng thái cửa</h2>
      <p>{{ door.status }} ({{ door.time }})</p>
    </div>

    <div>
      <h2>Nhiệt độ & Độ ẩm</h2>
      <p>Nhiệt độ: {{ temp.temperature }} °C</p>
      <p>Độ ẩm: {{ temp.humidity }} %</p>
      <p>Thời gian: {{ temp.time }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      button: { tohop: "-", time: "-" },
      door: { status: "-", time: "-" },
      temp: { temperature: "-", humidity: "-", time: "-" }
    };
  },
  methods: {
    async fetchAll() {
      try {
        const base = import.meta.env.VITE_API_URL || "http://localhost:5000";
        console.log("👉 Đang gọi API tới:", base);

        const [buttonRes, doorRes, tempRes] = await Promise.all([
          fetch(`${base}/api/latest`),
          fetch(`${base}/api/door`),
          fetch(`${base}/api/temp`)
        ]);

        this.button = await buttonRes.json();
        this.door = await doorRes.json();
        this.temp = await tempRes.json();
      } catch (err) {
        console.error("❌ Lỗi khi gọi API:", err);
      }
    }
  },
  mounted() {
    this.fetchAll();
    setInterval(this.fetchAll, 5000);
  }
};
</script>

<style>
h1 {
  text-align: center;
  margin-bottom: 20px;
}
div {
  margin: 10px 20px;
}
h2 {
  margin-top: 20px;
  color: #333;
}
</style>
