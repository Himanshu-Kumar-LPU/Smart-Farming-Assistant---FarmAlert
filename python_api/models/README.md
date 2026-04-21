# Multi-Model Files

The analyzer routes by image type and looks for these files:

- Leaf model: `leaf_model.keras` or `leaf_model.h5`
- Fruit model: `fruit_model.keras` or `fruit_model.h5`
- Whole plant model: `plant_model.keras` or `plant_model.h5`

Optional class name files:

- `fruit_class_names.json`
- `plant_class_names.json`

Expected class name format:

```json
["class_0", "class_1", "class_2"]
```

If a model for a detected type is missing, the API will return low confidence with guidance.
