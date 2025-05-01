<template>
  <div style="font-family: sans-serif; padding: 2rem;">
    <h1>🔵 CSW-2-J Sensor Monitor</h1>
    <p v-if="latest && latest.tohop !== '-'">
      <strong>Latest:</strong> {{ latest.tohop }}<br />
      <strong>Time:</strong> {{ latest.time }}
    </p>
    <p v-else>
      ⏳ Đang tải dữ liệu...
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      latest: { tohop: "-", time: "-" }
    };
  },
  methods: {
    async fetchData() {
      try {
        console.log("👉 Đang gọi API tới:", import.meta.env.VITE_API_URL);
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/latest`);
        if (!res.ok) throw new Error(`HTTP lỗi ${res.status}`);
        const data = await res.json();
        console.log("✅ Dữ liệu nhận được:", data);
        this.latest = data;
      } catch (err) {
        console.error("❌ Lỗi khi gọi API:", err.message);
      }
    }
  },
  mounted() {
  this.fetchData(); // gọi lần đầu
  setInterval(() => {
    this.fetchData(); // dùng arrow function để giữ đúng `this`
  }, 1000); // cập nhật mỗi 1 giây
}

}
</script>
