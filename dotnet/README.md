# C# / .NET

## Running

```bash
dotnet run --project dotnet/y2025 -- 1 
```

## Testing

```bash
dotnet test dotnet/y2025.unit
./dotnet/y2025.unit/test.sh 1 # run just day 1 with detailed output
```

- `--logger "console;verbosity=detailed"` more detailed output

### Logging

Tests hide a lot of logging. Using `Console.Error.WriteLine($"current: {current}, item: {item}");` will output logs.

### Debugging

`dotnet build dotnet/y2025.unit --configuration Debug`