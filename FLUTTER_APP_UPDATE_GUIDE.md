# Flutter App Update Guide - Missing Parameters

## ✅ API Status
The API has been updated to include all missing parameters. The following fields are now available in the API response:

## New Fields Added to API Response

### SWOT Analysis Fields
- `swotStrengths` (int?) - SWOT Strengths count
- `swotWeakness` (int?) - SWOT Weakness count  
- `swotOpportunities` (int?) - SWOT Opportunities count
- `swotThreats` (int?) - SWOT Threats count

### Additional Sector/Industry Metrics
- `sectorRoce` (double?) - Sector ROCE %
- `industryRoce` (double?) - Industry ROCE %
- `sectorRoe` (double?) - Sector ROE %
- `industryRoe` (double?) - Industry ROE %
- `sectorPegTtm` (double?) - Sector PEG TTM
- `industryPegTtm` (double?) - Industry PEG TTM
- `sectorNetProfitGrowthQtrQoq` (double?) - Sector Net Profit Growth Qtr QoQ %
- `sectorNetProfitGrowthAnnYoy` (double?) - Sector Net Profit Growth Ann YoY %
- `industryNetProfitGrowthQtrQoq` (double?) - Industry Net Profit Growth Qtr QoQ %
- `industryNetProfitGrowthAnnYoy` (double?) - Industry Net Profit Growth Ann YoY %
- `priceToBookAdjusted` (double?) - PBV Adjusted
- `fcEst1QForwardEbitQtr` (double?) - FC Est 1Q forward EBIT Qtr

## Flutter App Updates Required

### 1. Update Stock Model/Data Class

Add these fields to your stock model class:

```dart
class QualityStock {
  // ... existing fields ...
  
  // SWOT Analysis
  final int? swotStrengths;
  final int? swotWeakness;
  final int? swotOpportunities;
  final int? swotThreats;
  
  // Additional Sector/Industry Metrics
  final double? sectorRoce;
  final double? industryRoce;
  final double? sectorRoe;
  final double? industryRoe;
  final double? sectorPegTtm;
  final double? industryPegTtm;
  final double? sectorNetProfitGrowthQtrQoq;
  final double? sectorNetProfitGrowthAnnYoy;
  final double? industryNetProfitGrowthQtrQoq;
  final double? industryNetProfitGrowthAnnYoy;
  final double? priceToBookAdjusted;
  final double? fcEst1QForwardEbitQtr;
  
  QualityStock({
    // ... existing parameters ...
    this.swotStrengths,
    this.swotWeakness,
    this.swotOpportunities,
    this.swotThreats,
    this.sectorRoce,
    this.industryRoce,
    this.sectorRoe,
    this.industryRoe,
    this.sectorPegTtm,
    this.industryPegTtm,
    this.sectorNetProfitGrowthQtrQoq,
    this.sectorNetProfitGrowthAnnYoy,
    this.industryNetProfitGrowthQtrQoq,
    this.industryNetProfitGrowthAnnYoy,
    this.priceToBookAdjusted,
    this.fcEst1QForwardEbitQtr,
  });
  
  factory QualityStock.fromJson(Map<String, dynamic> json) {
    return QualityStock(
      // ... existing fields ...
      swotStrengths: json['swotStrengths'],
      swotWeakness: json['swotWeakness'],
      swotOpportunities: json['swotOpportunities'],
      swotThreats: json['swotThreats'],
      sectorRoce: json['sectorRoce']?.toDouble(),
      industryRoce: json['industryRoce']?.toDouble(),
      sectorRoe: json['sectorRoe']?.toDouble(),
      industryRoe: json['industryRoe']?.toDouble(),
      sectorPegTtm: json['sectorPegTtm']?.toDouble(),
      industryPegTtm: json['industryPegTtm']?.toDouble(),
      sectorNetProfitGrowthQtrQoq: json['sectorNetProfitGrowthQtrQoq']?.toDouble(),
      sectorNetProfitGrowthAnnYoy: json['sectorNetProfitGrowthAnnYoy']?.toDouble(),
      industryNetProfitGrowthQtrQoq: json['industryNetProfitGrowthQtrQoq']?.toDouble(),
      industryNetProfitGrowthAnnYoy: json['industryNetProfitGrowthAnnYoy']?.toDouble(),
      priceToBookAdjusted: json['priceToBookAdjusted']?.toDouble(),
      fcEst1QForwardEbitQtr: json['fcEst1QForwardEbitQtr']?.toDouble(),
    );
  }
}
```

### 2. Update UI to Display SWOT Analysis

Add a SWOT section in your stock details screen:

```dart
// SWOT Analysis Section
if (stock.swotStrengths != null || 
    stock.swotWeakness != null || 
    stock.swotOpportunities != null || 
    stock.swotThreats != null) {
  Card(
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('SWOT Analysis', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        SizedBox(height: 8),
        if (stock.swotStrengths != null)
          _buildSwotItem('Strengths', stock.swotStrengths!, Colors.green),
        if (stock.swotWeakness != null)
          _buildSwotItem('Weakness', stock.swotWeakness!, Colors.orange),
        if (stock.swotOpportunities != null)
          _buildSwotItem('Opportunities', stock.swotOpportunities!, Colors.blue),
        if (stock.swotThreats != null)
          _buildSwotItem('Threats', stock.swotThreats!, Colors.red),
      ],
    ),
  ),
}

Widget _buildSwotItem(String label, int count, Color color) {
  return Padding(
    padding: EdgeInsets.symmetric(vertical: 4),
    child: Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(label, style: TextStyle(fontWeight: FontWeight.w500)),
        Container(
          padding: EdgeInsets.symmetric(horizontal: 12, vertical: 4),
          decoration: BoxDecoration(
            color: color.withOpacity(0.2),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Text('$count', style: TextStyle(color: color, fontWeight: FontWeight.bold)),
        ),
      ],
    ),
  );
}
```

### 3. Update UI to Display Sector/Industry Comparisons

Add a comparison section showing stock metrics vs sector/industry:

```dart
// Sector/Industry Comparison Section
Card(
  child: Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Text('Sector & Industry Comparison', 
           style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
      SizedBox(height: 8),
      
      // ROCE Comparison
      if (stock.roce != null && stock.sectorRoce != null && stock.industryRoce != null)
        _buildComparisonRow(
          'ROCE',
          stock.roce!,
          stock.sectorRoce!,
          stock.industryRoce!,
        ),
      
      // ROE Comparison
      if (stock.roe != null && stock.sectorRoe != null && stock.industryRoe != null)
        _buildComparisonRow(
          'ROE',
          stock.roe!,
          stock.sectorRoe!,
          stock.industryRoe!,
        ),
      
      // PEG Comparison
      if (stock.pegTtm != null && stock.sectorPegTtm != null && stock.industryPegTtm != null)
        _buildComparisonRow(
          'PEG TTM',
          stock.pegTtm!,
          stock.sectorPegTtm!,
          stock.industryPegTtm!,
        ),
      
      // Net Profit Growth Comparison
      if (stock.sectorNetProfitGrowthAnnYoy != null && 
          stock.industryNetProfitGrowthAnnYoy != null)
        _buildComparisonRow(
          'Net Profit Growth (YoY)',
          stock.profitGrowthYoY,
          stock.sectorNetProfitGrowthAnnYoy!,
          stock.industryNetProfitGrowthAnnYoy!,
        ),
    ],
  ),
)

Widget _buildComparisonRow(String metric, double stockValue, 
                          double sectorValue, double industryValue) {
  return Padding(
    padding: EdgeInsets.symmetric(vertical: 8),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(metric, style: TextStyle(fontWeight: FontWeight.w600)),
        SizedBox(height: 4),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            _buildValueChip('Stock', stockValue, _getComparisonColor(stockValue, sectorValue)),
            _buildValueChip('Sector', sectorValue, Colors.grey),
            _buildValueChip('Industry', industryValue, Colors.grey),
          ],
        ),
      ],
    ),
  );
}

Widget _buildValueChip(String label, double value, Color color) {
  return Container(
    padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
    decoration: BoxDecoration(
      color: color.withOpacity(0.1),
      borderRadius: BorderRadius.circular(8),
      border: Border.all(color: color),
    ),
    child: Column(
      children: [
        Text(label, style: TextStyle(fontSize: 10, color: Colors.grey[600])),
        Text('${value.toStringAsFixed(2)}%', 
             style: TextStyle(fontWeight: FontWeight.bold, color: color)),
      ],
    ),
  );
}

Color _getComparisonColor(double stockValue, double sectorValue) {
  if (stockValue > sectorValue * 1.1) return Colors.green;
  if (stockValue < sectorValue * 0.9) return Colors.orange;
  return Colors.blue;
}
```

### 4. Display Additional Metrics

Add display for the new metrics:

```dart
// Additional Metrics Section
if (stock.priceToBookAdjusted != null || stock.fcEst1QForwardEbitQtr != null) {
  Card(
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Additional Metrics', 
             style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        SizedBox(height: 8),
        if (stock.priceToBookAdjusted != null)
          _buildMetricRow('PBV Adjusted', stock.priceToBookAdjusted!.toStringAsFixed(2)),
        if (stock.fcEst1QForwardEbitQtr != null)
          _buildMetricRow('FC Est 1Q Forward EBIT Qtr', 
                         stock.fcEst1QForwardEbitQtr!.toStringAsFixed(2)),
      ],
    ),
  ),
}
```

## Testing

1. **Verify API Response**: Test the API endpoint to confirm new fields are returned:
   ```bash
   curl http://your-api-url/api/quality-stocks/stock/RELIANCE
   ```

2. **Update Flutter Model**: Add fields to your model class

3. **Update UI**: Add UI components to display the new fields

4. **Handle Null Values**: All new fields are optional, so handle null cases appropriately

## Example API Response

The API now returns responses like this:

```json
{
  "stockName": "RELIANCE",
  "nseCode": "RELIANCE",
  "swotStrengths": 15,
  "swotWeakness": 12,
  "swotOpportunities": 9,
  "swotThreats": 3,
  "sectorRoce": 24.97,
  "industryRoce": 35.28,
  "sectorRoe": 27.07,
  "industryRoe": 47.23,
  "sectorPegTtm": 1.46,
  "industryPegTtm": 0.2,
  "sectorNetProfitGrowthQtrQoq": -10.1,
  "sectorNetProfitGrowthAnnYoy": 45.32,
  "industryNetProfitGrowthQtrQoq": -2.96,
  "industryNetProfitGrowthAnnYoy": 66.85,
  "priceToBookAdjusted": 5.62,
  "fcEst1QForwardEbitQtr": 5884.18,
  // ... other existing fields ...
}
```

## Next Steps

1. ✅ API updated - All fields are now available
2. ⏳ Update Flutter model class
3. ⏳ Update Flutter UI to display SWOT analysis
4. ⏳ Update Flutter UI to display sector/industry comparisons
5. ⏳ Test the integration

The API is ready - you just need to update the Flutter app to consume and display these new fields!

