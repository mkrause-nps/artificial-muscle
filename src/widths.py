#!/usr/bin/env python3


class Widths:
    specs = {
        'perp_sm': {
            'before': {
                'status': 'prior',
                'print_direction': 'perpendicular',
                'material': 'sacrificial_material'
            },
            'after': {
                'status': 'past',
                'print_direction': 'perpendicular',
                'material': 'sacrificial_material'
            },
            'suffix': 'perp_sm'
        },
        'perp_br': {
            'before': {
                'status': 'prior',
                'print_direction': 'perpendicular',
                'material': 'black_resin'
            },
            'after': {
                'status': 'past',
                'print_direction': 'perpendicular',
                'material': 'black_resin'
            },
            'suffix': 'perp_br'
        },
        'para_sm': {
            'before': {
                'status': 'prior',
                'print_direction': 'parallel',
                'material': 'sacrificial_material'
            },
            'after': {
                'status': 'past',
                'print_direction': 'parallel',
                'material': 'sacrificial_material'
            },
            'suffix': 'para_sm'
        },
        'para_br': {
            'before': {
                'status': 'prior',
                'print_direction': 'parallel',
                'material': 'black_resin'
            },
            'after': {
                'status': 'past',
                'print_direction': 'parallel',
                'material': 'black_resin'
            },
            'suffix': 'para_br'
        }
    }
