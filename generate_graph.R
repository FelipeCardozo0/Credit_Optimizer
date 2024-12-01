print("Arguments:")
print(args)

if (length(args) < 2) {
    stop("Error: Insufficient arguments provided.")
}

input_file <- args[1]
output_file <- args[2]

print("Input file:")
print(input_file)

print("Output file:")
print(output_file)

if (!file.exists(input_file)) {
    stop("Error: Input file does not exist.")
}

data <- read_csv(input_file)
print("Data read successfully:")
print(data)

if (!all(c("credit_score", "income") %in% colnames(data))) {
    stop("Error: Required columns missing from input file.")
}

plot <- ggplot(data, aes(x = credit_score, y = income)) +
  geom_point(color = 'blue') +
  labs(title = "Credit Score vs Income", x = "Credit Score", y = "Income") +
  theme_minimal()

ggsave(output_file, plot)
print("Plot saved successfully.")
