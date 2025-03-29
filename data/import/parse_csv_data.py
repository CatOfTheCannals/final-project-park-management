#!/usr/bin/env python3
"""
CSV Parser for Park Management Database

This script parses the provided CSV files and generates appropriate data for the database.
"""

import csv
import os
import re

# Create the import directory if it doesn't exist
os.makedirs('data/import', exist_ok=True)

def clean_csv_line(line):
    """Clean a CSV line from the provided format to standard CSV format."""
    # Remove leading/trailing whitespace
    line = line.strip()
    # Skip empty lines or header lines
    if not line or line.startswith('"jurisdicción"') or line.startswith('"grupo"') or line.startswith('"año"'):
        return None
    # Remove quotes and replace with proper CSV format
    line = re.sub(r'"([^"]*)";"([^"]*)";"([^"]*)";"([^"]*)"', r'"\1","\2","\3","\4"', line)
    line = re.sub(r'"([^"]*)";"([^"]*)";"([^"]*)"', r'"\1","\2","\3"', line)
    return line

def parse_areas_protegidas():
    """Parse areas_protegidas_nacionales_y_provinciales_por_jurisdiccion.csv."""
    provinces = []
    
    with open('data/areas_protegidas_nacionales_y_provinciales_por_jurisdiccion.csv', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        clean_line = clean_csv_line(line)
        if not clean_line:
            continue
        
        # Parse the CSV line
        parts = clean_line.split('","')
        if len(parts) >= 3:
            province_name = parts[0].strip('"')
            # Skip non-province lines
            if province_name in ["Áreas Marinas Protegidas", "Espacio marítimo argentino"]:
                continue
            
            # Add to provinces list
            provinces.append({
                'name': province_name,
                'responsible_organization': f"Organismo de Conservación de {province_name}"
            })
    
    # Write provinces to CSV
    with open('data/import/provinces.csv', 'w', encoding='utf-8') as f:
        f.write('id,name,responsible_organization\n')
        for i, province in enumerate(provinces, 1):
            f.write(f'{i},"{province["name"]}","{province["responsible_organization"]}"\n')
    
    print(f"Generated {len(provinces)} provinces")

def parse_representatividad_especies():
    """Parse representatividad_de_las_especies_en_areas_protegidas_nacionales.csv."""
    species_groups = []
    
    with open('data/representatividad_de_las_especies_en_areas_protegidas_nacionales.csv', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        clean_line = clean_csv_line(line)
        if not clean_line:
            continue
        
        # Parse the CSV line
        parts = clean_line.split('","')
        if len(parts) >= 3:
            group_name = parts[0].strip('"')
            # Skip the "Total" line
            if group_name == "Total":
                continue
            
            # Add to species groups list
            species_groups.append({
                'name': group_name,
                'count_argentina': parts[1].strip('"'),
                'count_protected': parts[2].strip('"'),
                'percentage': parts[3].strip('"') if len(parts) > 3 else "0"
            })
    
    # Write species groups info to a file for reference
    with open('data/import/species_groups_info.csv', 'w', encoding='utf-8') as f:
        f.write('name,count_argentina,count_protected,percentage\n')
        for group in species_groups:
            f.write(f'{group["name"]},{group["count_argentina"]},{group["count_protected"]},{group["percentage"]}\n')
    
    print(f"Generated info for {len(species_groups)} species groups")

def parse_visitantes():
    """Parse visitantes_registrados_en_los_parques_nacionales.csv."""
    visitor_stats = []
    
    with open('data/visitantes_registrados_en_los_parques_nacionales.csv', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        clean_line = clean_csv_line(line)
        if not clean_line:
            continue
        
        # Parse the CSV line
        parts = clean_line.split('","')
        if len(parts) >= 3:
            year = parts[0].strip('"')
            residents_pct = parts[1].strip('"')
            non_residents_pct = parts[2].strip('"')
            
            # Add to visitor stats list
            visitor_stats.append({
                'year': year,
                'residents_pct': residents_pct,
                'non_residents_pct': non_residents_pct
            })
    
    # Write visitor stats to a file for reference
    with open('data/import/visitor_stats.csv', 'w', encoding='utf-8') as f:
        f.write('year,residents_pct,non_residents_pct\n')
        for stat in visitor_stats:
            f.write(f'{stat["year"]},{stat["residents_pct"]},{stat["non_residents_pct"]}\n')
    
    print(f"Generated visitor stats for {len(visitor_stats)} years")

def main():
    """Main function to parse all CSV files."""
    print("Parsing CSV files...")
    parse_areas_protegidas()
    parse_representatividad_especies()
    parse_visitantes()
    print("Done parsing CSV files.")

if __name__ == "__main__":
    main()
