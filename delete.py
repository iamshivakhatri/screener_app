async  loadData() {
  try {
    const response = await fetch("/static/test.json");
    const data = await response.json();

    // Assuming you're working with TSLA data as before
    const tslaData = data.TSLA.values;

    console.log("Data fetched successfully:", tslaData);

    // Map the data to convert string values to numbers
    this.klines = tslaData.map((item) => ({
      time: Math.floor(new Date(item.datetime).getTime() / 1000),
      open: parseFloat(item.open),
      high: parseFloat(item.high),
      low: parseFloat(item.low),
      close: parseFloat(item.close),
      volume: parseInt(item.volume, 10), // Convert volume to integer
    }));

    console.log("Data loaded successfully:", this.klines);

    this.xspan = this.klines
      .map((item) => item.time)
      .map((d, i, arr) => (i ? arr[i] - arr[i - 1] : 0))[2];

    const prebars = [...new Array(100)].map((_, i) => ({
      time: this.klines[0].time - (i + 1) * this.xspan,
    }));

    const postbars = [...new Array(100)].map((_, i) => ({
      time: this.klines[this.klines.length - 1].time + (i + 1) * this.xspan,
    }));

    // Set the data to the chart
    this.candleseries.setData([...prebars, ...this.klines, ...postbars]);
  } catch (error) {
    console.error("Error fetching or parsing data:", error);
  }
}

# 1685557800
# 1724356740


# 1685597880
# 1724347620