sales <- matrix(
  c(120,150,130,160,
    100,140,120,150,
    90,110,100,130),
  nrow=3,
  byrow=TRUE)

price <- matrix(
  c(10,10,10,10,
    12,12,12,12,
    8,8,8,8),
  nrow=3,
  byrow=TRUE)

revenue <- sales * price
revenue

region_revenue <- rowSums(revenue)
region_revenue