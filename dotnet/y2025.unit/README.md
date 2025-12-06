# Test Configuration

## Simplified Output

For cleaner test output, use:

```bash
dotnet test dotnet/y2025.unit --nologo --verbosity minimal
```

This will show only:
- Test run summary
- Failed tests (if any)
- Final pass/fail status

## Verbosity Levels

- `quiet` - Minimal output (recommended)
- `minimal` - Shows test names
- `normal` - Default, shows more details
- `detailed` - Full output with timings
- `diagnostic` - Maximum verbosity for debugging

## Other Useful Options

- `--nologo` - Suppress Microsoft and .NET logos
- `--filter "FullyQualifiedName~TestName"` - Run specific tests
- `--list-tests` - List all tests without running them

## Filtering Tests

Class Name

`dotnet test --filter "FullyQualifiedName~Day1Tests"`

Namespace

`dotnet test --filter "FullyQualifiedName~y2025.unit.day_1"`

DisplayName

`dotnet test --filter "DisplayName~Day1"`


| Filter   | Example                                                            |
| -------- | ------------------------------------------------------------------ |
| Contains | `--filter "FullyQualifiedName~day_1"`                              |
| Equals   | `--filter "ClassName=Day1Tests"`                                   |
| Multiple | `--filter "FullyQualifiedName~day_1 \| FullyQualifiedName~day_2"`  | 