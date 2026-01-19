# Development Guide

Guide for developers working on the College Basketball Ratings project.

## Architecture Overview

### System Components

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   React     │─────▶│   Flask     │─────▶│  CBBD API   │      │  Supabase   │
│  Frontend   │      │   Backend   │      │             │      │  Database   │
│             │◀─────│             │─────▶│             │      │             │
└─────────────┘      └─────────────┘      └─────────────┘      └─────────────┘
      │                     │                                           │
      │                     │                                           │
      └─────────────────────┴───────────────────────────────────────────┘
                   Data Flow: Fetch → Calculate → Store → Display
```

### Data Flow

1. **User Action** → Clicks "Refresh Data"
2. **Frontend** → POST to `/api/refresh`
3. **Backend** → Fetches from CBBD API
4. **Backend** → Calculates ratings
5. **Backend** → Stores in Supabase
6. **Backend** → Returns success
7. **Frontend** → GET from `/api/teams`
8. **Frontend** → Renders table

## Code Organization

### Backend (`api/`)

**`fetch_data.py`** - Data fetching layer
- `CBBDataFetcher` class handles CBBD API calls
- Methods: `fetch_team_stats()`, `fetch_adjusted_efficiency()`
- Data validation: `validate_team_data()`

**`calculate_ratings.py`** - Rating calculation engine
- `RatingCalculator` class implements Four Factors
- Methods: `calculate_offensive_rating()`, `calculate_defensive_rating()`
- Ranking: `process_teams()`, `_add_component_ranks()`

**`app.py`** - Flask API server
- Routes: `/api/teams`, `/api/refresh`, etc.
- Supabase integration
- Error handling

### Frontend (`frontend/src/`)

**`App.js`** - Main application component
- State management for teams, loading, errors
- API calls to backend
- Layout structure

**`components/TeamTable.jsx`** - Interactive table
- TanStack Table for sorting
- Row click handlers
- Responsive design

**`components/TeamDetail.jsx`** - Expanded team view
- Dynamic team colors
- Four factors breakdown
- Rank display

**`components/RefreshButton.jsx`** - Data refresh UI
- Loading states
- Icon animation

## Adding New Features

### Adding a New Metric

1. **Update Database Schema** (`database/schema.sql`)
   ```sql
   ALTER TABLE team_ratings
   ADD COLUMN new_metric DECIMAL(5,2);
   ```

2. **Update Rating Calculator** (`api/calculate_ratings.py`)
   ```python
   def calculate_new_metric(self, team: Dict) -> float:
       # Your calculation logic
       return value
   ```

3. **Update API Response** (`api/app.py`)
   ```python
   record = {
       # ... existing fields ...
       'new_metric': team.get('new_metric'),
   }
   ```

4. **Add to Frontend Table** (`frontend/src/components/TeamTable.jsx`)
   ```javascript
   {
       accessorKey: 'new_metric',
       header: 'New Metric',
       cell: (info) => info.getValue()?.toFixed(1),
   }
   ```

5. **Display in Detail View** (`frontend/src/components/TeamDetail.jsx`)
   ```javascript
   <div className="factor-item">
       <span className="factor-label">New Metric</span>
       <span className="factor-value">
           {team.new_metric?.toFixed(1)}
       </span>
   </div>
   ```

### Adding a New API Endpoint

1. **Define Route** (`api/app.py`)
   ```python
   @app.route('/api/your-endpoint', methods=['GET'])
   def your_endpoint():
       # Implementation
       return jsonify({'data': result})
   ```

2. **Add Frontend Call** (`frontend/src/App.js` or component)
   ```javascript
   const fetchData = async () => {
       const response = await fetch(`${API_BASE_URL}/api/your-endpoint`);
       const data = await response.json();
       // Handle data
   };
   ```

### Adding a New Component

1. **Create Component File** (`frontend/src/components/YourComponent.jsx`)
   ```javascript
   import React from 'react';
   import './YourComponent.css';

   function YourComponent({ props }) {
       return (
           <div className="your-component">
               {/* Your JSX */}
           </div>
       );
   }

   export default YourComponent;
   ```

2. **Create Styles** (`frontend/src/components/YourComponent.css`)
   ```css
   .your-component {
       /* Your styles */
   }
   ```

3. **Import and Use** (in parent component)
   ```javascript
   import YourComponent from './components/YourComponent';

   // In JSX:
   <YourComponent prop={value} />
   ```

## Customizing Rating Formula

### Adjust Weights

Edit `api/calculate_ratings.py`:

```python
class RatingCalculator:
    # Overall weights
    OFFENSIVE_WEIGHT = 0.52  # Change this
    DEFENSIVE_WEIGHT = 0.48  # And this

    # Four Factors weights
    EFG_WEIGHT = 0.40  # Adjust these
    ORB_WEIGHT = 0.20
    TOV_WEIGHT = 0.25
    FTR_WEIGHT = 0.15
```

### Add New Factor

1. **Fetch Data** - Ensure CBBD API provides it
2. **Store in Database** - Add column
3. **Calculate Rating** - Update formula
4. **Display** - Add to frontend

## Testing

### Backend Tests

```python
# Test data fetching
python api/fetch_data.py

# Test calculations
python api/calculate_ratings.py

# Test with sample data
if __name__ == "__main__":
    test_team = {...}
    calculator = RatingCalculator()
    ratings = calculator.calculate_all_ratings(test_team)
    print(ratings)
```

### Frontend Tests

```bash
# Run test suite
cd frontend
npm test

# Manual testing
npm start
# Then check browser console for errors
```

### Integration Tests

1. Start backend: `python api/app.py`
2. Start frontend: `npm start`
3. Click "Refresh Data"
4. Verify data loads
5. Check browser Network tab
6. Verify Supabase records

## Common Modifications

### Change Team Colors

Edit `frontend/src/components/TeamDetail.css`:

```css
.team-detail {
    background: linear-gradient(
        135deg,
        var(--team-primary, #YourColor1) 0%,
        var(--team-secondary, #YourColor2) 100%
    );
}
```

### Adjust Table Columns

Edit `frontend/src/components/TeamTable.jsx`:

```javascript
const columns = useMemo(() => [
    // Add, remove, or modify column definitions
    {
        accessorKey: 'field_name',
        header: 'Display Name',
        cell: (info) => info.getValue(),
        size: 100,  // Column width
    },
], []);
```

### Change Sorting Default

Edit `frontend/src/components/TeamTable.jsx`:

```javascript
const [sorting, setSorting] = useState([
    { id: 'your_field', desc: true }  // Change this
]);
```

### Modify API Response Format

Edit `api/app.py`:

```python
return jsonify({
    'success': True,
    'count': len(data),
    'teams': data,
    # Add custom fields here
})
```

## Performance Optimization

### Backend

- Use connection pooling for Supabase
- Cache CBBD API responses
- Batch database inserts
- Add pagination to `/api/teams`

### Frontend

- Implement virtual scrolling for large tables
- Lazy load team details
- Add service worker for offline support
- Optimize images and assets

### Database

- Ensure indexes exist (check `schema.sql`)
- Monitor query performance in Supabase
- Archive old seasons

## Debugging

### Backend Issues

```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# In your code:
logging.debug(f"Team data: {team}")
```

### Frontend Issues

```javascript
// Add console debugging
console.log('Teams data:', teams);
console.error('Error occurred:', error);

// Use React DevTools browser extension
```

### API Issues

```bash
# Test endpoints directly
curl http://localhost:5000/api/health
curl http://localhost:5000/api/teams

# Check Supabase logs in dashboard
```

## Environment-Specific Config

### Development
- Local database (optional)
- Verbose logging
- Hot reload enabled
- CORS open

### Production
- Supabase production project
- Error logging only
- Optimized builds
- CORS restricted

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Keep functions focused and small

### JavaScript
- Use functional components
- Follow React hooks best practices
- Use meaningful variable names
- Keep components under 300 lines

### CSS
- Use BEM-like naming
- Group related styles
- Comment complex styles
- Use CSS variables for themes

## Contributing Workflow

1. Create feature branch
2. Make changes
3. Test locally
4. Update documentation
5. Commit with clear message
6. Push and create PR
7. Review and merge

## Resources

- **CBBD API Docs:** [collegebasketballdata.com](https://collegebasketballdata.com)
- **React Docs:** [react.dev](https://react.dev)
- **TanStack Table:** [tanstack.com/table](https://tanstack.com/table)
- **Flask Docs:** [flask.palletsprojects.com](https://flask.palletsprojects.com)
- **Supabase Docs:** [supabase.com/docs](https://supabase.com/docs)

## Getting Help

1. Check SETUP.md for setup issues
2. Review this guide for development questions
3. Search GitHub issues
4. Check component documentation
5. Review CBBD API docs for data questions

---

**Happy Coding!**
