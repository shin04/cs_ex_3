@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@m = common global i32 0, align 4
@n = common global i32 0, align 4
define i32 @power(i32, i32){
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 %1, i32* %4, align 4
  %5 = alloca i32, align 4
  store i32 %0, i32* %5, align 4
  %6 = load i32, i32* %3, align 4
  %7 = icmp sle i32 %6, 0
  br i1 %7, label %8, label %9
  8:
  store i32 1, i32* %3, align 4
  br label %16
  9:
  %10 = load i32, i32* %2, align 4
  %11 = load i32, i32* %3, align 4
  %12 = sub nsw i32 %11, 1
  %13 = call i32 @power(i32 %12, i32 %10)
  %14 = load i32, i32* %2, align 4
  %15 = mul nsw i32 %13, %14
  store i32 %15, i32* %3, align 4
  br label %16
  16:
  %17 = load i32, i32* %3, align 4
  ret i32 %17
}
define i32 @main(){
  %1 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* @m)
  %2 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* @n)
  %3 = load i32, i32* @m, align 4
  %4 = load i32, i32* @n, align 4
  %5 = call i32 @power(i32 %4, i32 %3)
  %6 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32 %5)
  ret i32 %0
}
declare i32 @scanf(i8*, ...)
declare i32 @printf(i8*, ...)
